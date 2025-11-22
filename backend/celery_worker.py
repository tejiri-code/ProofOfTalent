"""
Celery worker for background task processing
Handles CV processing asynchronously
"""

from celery import Celery
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from cv_analyzer import (
    parse_pdf_cv, parse_cv, analyze_candidate_comprehensive,
    train_visa_models, generate_synthetic_training_data
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery(
    'cv_analysis',
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes
    task_soft_time_limit=540,  # 9 minutes
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cv_analysis.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models (assuming they're in main.py)
from main import CVAnalysis, MODELS

@celery_app.task(bind=True, name='process_cv')
def process_cv_task(self, analysis_id: int, file_path: str):
    """
    Process CV asynchronously
    """
    db = SessionLocal()
    
    try:
        logger.info(f"Starting CV processing for analysis_id: {analysis_id}")
        
        # Update status
        self.update_state(state='PROCESSING', meta={'progress': 10})
        
        # Parse CV
        logger.info(f"Parsing PDF: {file_path}")
        text = parse_pdf_cv(file_path)
        self.update_state(state='PROCESSING', meta={'progress': 30})
        
        # Extract structured data
        logger.info("Extracting structured data")
        parsed = parse_cv(text)
        self.update_state(state='PROCESSING', meta={'progress': 50})
        
        # Analyze
        logger.info("Running comprehensive analysis")
        result = analyze_candidate_comprehensive(parsed, MODELS)
        self.update_state(state='PROCESSING', meta={'progress': 80})
        
        # Update database
        logger.info("Updating database")
        analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
        if analysis:
            analysis.features = result.get('features', {})
            analysis.visa_analysis = result.get('visa_analysis', {})
            analysis.external_data = result.get('external_data', {})
            analysis.processing_status = "completed"
            db.commit()
            
        self.update_state(state='PROCESSING', meta={'progress': 100})
        
        logger.info(f"Successfully completed CV processing for analysis_id: {analysis_id}")
        return {
            'status': 'completed',
            'analysis_id': analysis_id,
            'features_count': len(result.get('features', {})),
            'visas_analyzed': len(result.get('visa_analysis', {}))
        }
        
    except Exception as e:
        logger.error(f"Error processing CV {analysis_id}: {e}")
        
        # Update database with error
        analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
        if analysis:
            analysis.processing_status = "failed"
            analysis.error_message = str(e)
            db.commit()
        
        # Re-raise for Celery to handle
        raise
        
    finally:
        db.close()

@celery_app.task(name='batch_process_cvs')
def batch_process_cvs_task(analysis_ids: list):
    """
    Process multiple CVs in parallel
    """
    from celery import group
    
    job = group([
        process_cv_task.s(aid, f"uploaded_cvs/{aid}.pdf") 
        for aid in analysis_ids
    ])
    
    result = job.apply_async()
    return {
        'status': 'queued',
        'total_tasks': len(analysis_ids),
        'job_id': result.id
    }

@celery_app.task(name='retrain_models')
def retrain_models_task(n_samples: int = 500):
    """
    Retrain ML models with fresh synthetic data
    """
    db = SessionLocal()
    
    try:
        logger.info(f"Starting model retraining with {n_samples} samples")
        
        # Generate training data
        from main import ModelMetrics
        training_data = generate_synthetic_training_data(n_samples=n_samples)
        
        # Train models
        global MODELS
        new_models = train_visa_models(training_data)
        
        # Update global models
        MODELS.update(new_models)
        
        # Save metrics
        for visa, model_info in new_models.items():
            metric = ModelMetrics(
                visa_type=visa,
                auc_score=model_info['auc'],
                feature_importances=model_info['feature_importances']
            )
            db.add(metric)
        
        db.commit()
        
        logger.info(f"Successfully retrained {len(new_models)} models")
        return {
            'status': 'completed',
            'models_trained': len(new_models),
            'avg_auc': sum(m['auc'] for m in new_models.values()) / len(new_models)
        }
        
    except Exception as e:
        logger.error(f"Error retraining models: {e}")
        raise
        
    finally:
        db.close()

@celery_app.task(name='cleanup_old_files')
def cleanup_old_files_task(days_old: int = 30):
    """
    Clean up old CV files
    """
    from pathlib import Path
    from datetime import datetime, timedelta
    
    db = SessionLocal()
    upload_dir = Path("uploaded_cvs")
    cutoff_date = datetime.utcnow() - timedelta(days=days_old)
    
    try:
        deleted_count = 0
        
        # Find old analyses
        old_analyses = db.query(CVAnalysis).filter(
            CVAnalysis.upload_date < cutoff_date
        ).all()
        
        for analysis in old_analyses:
            file_path = upload_dir / analysis.filename
            
            # Delete file if exists
            if file_path.exists():
                file_path.unlink()
                deleted_count += 1
            
            # Delete database record
            db.delete(analysis)
        
        db.commit()
        
        logger.info(f"Cleaned up {deleted_count} old files")
        return {
            'status': 'completed',
            'files_deleted': deleted_count,
            'cutoff_date': cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up files: {e}")
        raise
        
    finally:
        db.close()

# Periodic tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Set up periodic tasks
    """
    from celery.schedules import crontab
    
    # Retrain models daily at 2 AM
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        retrain_models_task.s(),
        name='daily-model-retrain'
    )
    
    # Clean up old files weekly
    sender.add_periodic_task(
        crontab(hour=3, minute=0, day_of_week=1),
        cleanup_old_files_task.s(days_old=30),
        name='weekly-cleanup'
    )

if __name__ == '__main__':
    celery_app.start()