"""
FastAPI Backend for CV Analysis System
Main application entry point
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import os
import json
from datetime import datetime
import logging
from pathlib import Path

# Database
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Your CV analysis module (assuming it's saved as cv_analyzer.py)
import sys
sys.path.append('.')
from cv_analyzer import (
    parse_pdf_cv, parse_cv, analyze_candidate_comprehensive,
    train_visa_models, generate_synthetic_training_data, VISAS
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CV Analysis API",
    description="Multi-domain CV analysis with visa eligibility prediction",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cv_analysis.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class CVAnalysis(Base):
    __tablename__ = "cv_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    features = Column(JSON)
    visa_analysis = Column(JSON)
    external_data = Column(JSON)
    processing_status = Column(String, default="pending")
    error_message = Column(String, nullable=True)
    
class ModelMetrics(Base):
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    visa_type = Column(String, index=True)
    auc_score = Column(Float)
    training_date = Column(DateTime, default=datetime.utcnow)
    feature_importances = Column(JSON)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Global model storage
MODELS = {}
UPLOAD_DIR = Path("uploaded_cvs")
UPLOAD_DIR.mkdir(exist_ok=True)

# Pydantic models for API
class AnalysisResponse(BaseModel):
    id: int
    filename: str
    processing_status: str
    upload_date: datetime
    features: Optional[Dict[str, Any]] = None
    visa_analysis: Optional[Dict[str, Any]] = None
    
class VisaRecommendation(BaseModel):
    visa_type: str
    likelihood: float
    recommendation: str
    gaps_count: int
    timeline_weeks: int
    confidence: str

class BatchUploadResponse(BaseModel):
    uploaded_files: List[str]
    total_count: int
    message: str

class ComparisonRequest(BaseModel):
    candidate_ids: List[int]
    visa_type: str = "uk_global_talent"

# Startup event - Train models
@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    logger.info("Starting up CV Analysis API...")
    
    try:
        # Generate training data
        logger.info("Generating training data...")
        training_data = generate_synthetic_training_data(n_samples=500)
        
        # Train models
        logger.info("Training models...")
        global MODELS
        MODELS = train_visa_models(training_data)
        logger.info(f"Successfully trained {len(MODELS)} visa models")
        
        # Save metrics to database
        db = SessionLocal()
        try:
            for visa, model_info in MODELS.items():
                metric = ModelMetrics(
                    visa_type=visa,
                    auc_score=model_info['auc'],
                    feature_importances=model_info['feature_importances']
                )
                db.add(metric)
            db.commit()
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error during startup: {e}")

# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CV Analysis API",
        "version": "1.0.0",
        "models_loaded": len(MODELS),
        "supported_visas": VISAS
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "models": {
            visa: {
                "loaded": True,
                "auc": model_info.get('auc', 0)
            }
            for visa, model_info in MODELS.items()
        }
    }

# CV Upload and Analysis
@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_cv(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Upload and analyze a single CV
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save file
    file_path = UPLOAD_DIR / file.filename
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Create database record
    db_analysis = CVAnalysis(
        filename=file.filename,
        processing_status="processing"
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    # Process CV in background
    if background_tasks:
        background_tasks.add_task(process_cv_task, db_analysis.id, str(file_path))
    else:
        # Process synchronously if no background tasks
        await process_cv_sync(db_analysis.id, str(file_path), db)
    
    return AnalysisResponse(
        id=db_analysis.id,
        filename=db_analysis.filename,
        processing_status=db_analysis.processing_status,
        upload_date=db_analysis.upload_date
    )

async def process_cv_sync(analysis_id: int, file_path: str, db: Session):
    """Process CV synchronously"""
    try:
        # Parse CV
        text = parse_pdf_cv(file_path)
        parsed = parse_cv(text)
        
        # Analyze
        result = analyze_candidate_comprehensive(parsed, MODELS)
        
        # Update database
        analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
        if analysis:
            analysis.features = result.get('features', {})
            analysis.visa_analysis = result.get('visa_analysis', {})
            analysis.external_data = result.get('external_data', {})
            analysis.processing_status = "completed"
            db.commit()
            
    except Exception as e:
        logger.error(f"Error processing CV {analysis_id}: {e}")
        analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
        if analysis:
            analysis.processing_status = "failed"
            analysis.error_message = str(e)
            db.commit()

def process_cv_task(analysis_id: int, file_path: str):
    """Background task for CV processing"""
    db = SessionLocal()
    try:
        # Parse CV
        text = parse_pdf_cv(file_path)
        parsed = parse_cv(text)
        
        # Analyze
        result = analyze_candidate_comprehensive(parsed, MODELS)
        
        # Update database
        analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
        if analysis:
            analysis.features = result.get('features', {})
            analysis.visa_analysis = result.get('visa_analysis', {})
            analysis.external_data = result.get('external_data', {})
            analysis.processing_status = "completed"
            db.commit()
            
    except Exception as e:
        logger.error(f"Error processing CV {analysis_id}: {e}")
        analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
        if analysis:
            analysis.processing_status = "failed"
            analysis.error_message = str(e)
            db.commit()
    finally:
        db.close()

@app.post("/api/v1/batch-upload", response_model=BatchUploadResponse)
async def batch_upload(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Upload multiple CVs for batch processing
    """
    uploaded = []
    
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            continue
            
        file_path = UPLOAD_DIR / file.filename
        try:
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Create database record
            db_analysis = CVAnalysis(
                filename=file.filename,
                processing_status="processing"
            )
            db.add(db_analysis)
            db.commit()
            db.refresh(db_analysis)
            
            # Queue for processing
            if background_tasks:
                background_tasks.add_task(process_cv_task, db_analysis.id, str(file_path))
            
            uploaded.append(file.filename)
            
        except Exception as e:
            logger.error(f"Error uploading {file.filename}: {e}")
    
    return BatchUploadResponse(
        uploaded_files=uploaded,
        total_count=len(uploaded),
        message=f"Successfully queued {len(uploaded)} CVs for processing"
    )

@app.get("/api/v1/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get analysis results by ID
    """
    analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return AnalysisResponse(
        id=analysis.id,
        filename=analysis.filename,
        processing_status=analysis.processing_status,
        upload_date=analysis.upload_date,
        features=analysis.features,
        visa_analysis=analysis.visa_analysis
    )

@app.get("/api/v1/analyses", response_model=List[AnalysisResponse])
async def list_analyses(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all analyses with optional filtering
    """
    query = db.query(CVAnalysis)
    
    if status:
        query = query.filter(CVAnalysis.processing_status == status)
    
    analyses = query.offset(skip).limit(limit).all()
    
    return [
        AnalysisResponse(
            id=a.id,
            filename=a.filename,
            processing_status=a.processing_status,
            upload_date=a.upload_date,
            features=a.features,
            visa_analysis=a.visa_analysis
        )
        for a in analyses
    ]

@app.get("/api/v1/recommendations/{analysis_id}", response_model=List[VisaRecommendation])
async def get_recommendations(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get visa recommendations sorted by likelihood
    """
    analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if not analysis.visa_analysis:
        raise HTTPException(status_code=400, detail="Analysis not yet completed")
    
    recommendations = []
    for visa, data in analysis.visa_analysis.items():
        recommendations.append(
            VisaRecommendation(
                visa_type=visa,
                likelihood=data.get('likelihood', 0),
                recommendation=data.get('recommendation', 'unknown'),
                gaps_count=len(data.get('gaps_identified', [])),
                timeline_weeks=data.get('timeline', {}).get('projected_completion_weeks', 0),
                confidence=data.get('confidence', 'unknown')
            )
        )
    
    # Sort by likelihood
    recommendations.sort(key=lambda x: x.likelihood, reverse=True)
    
    return recommendations

@app.post("/api/v1/compare")
async def compare_candidates(request: ComparisonRequest, db: Session = Depends(get_db)):
    """
    Compare multiple candidates for a specific visa
    """
    analyses = db.query(CVAnalysis).filter(
        CVAnalysis.id.in_(request.candidate_ids)
    ).all()
    
    if not analyses:
        raise HTTPException(status_code=404, detail="No analyses found")
    
    comparison = []
    for analysis in analyses:
        if not analysis.visa_analysis:
            continue
            
        visa_data = analysis.visa_analysis.get(request.visa_type, {})
        comparison.append({
            'id': analysis.id,
            'filename': analysis.filename,
            'likelihood': visa_data.get('likelihood', 0),
            'experience': analysis.features.get('years_experience', 0) if analysis.features else 0,
            'skills': analysis.features.get('total_skills', 0) if analysis.features else 0,
            'gaps': len(visa_data.get('gaps_identified', [])),
            'timeline_weeks': visa_data.get('timeline', {}).get('projected_completion_weeks', 0)
        })
    
    # Sort by likelihood
    comparison.sort(key=lambda x: x['likelihood'], reverse=True)
    
    return {
        'visa_type': request.visa_type,
        'comparison': comparison
    }

@app.get("/api/v1/models/metrics")
async def get_model_metrics(db: Session = Depends(get_db)):
    """
    Get current model performance metrics
    """
    metrics = db.query(ModelMetrics).order_by(ModelMetrics.training_date.desc()).limit(len(VISAS)).all()
    
    return {
        'models': [
            {
                'visa_type': m.visa_type,
                'auc_score': m.auc_score,
                'training_date': m.training_date.isoformat(),
                'feature_importances': m.feature_importances
            }
            for m in metrics
        ]
    }

@app.delete("/api/v1/analysis/{analysis_id}")
async def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Delete an analysis record
    """
    analysis = db.query(CVAnalysis).filter(CVAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Delete file if exists
    file_path = UPLOAD_DIR / analysis.filename
    if file_path.exists():
        file_path.unlink()
    
    db.delete(analysis)
    db.commit()
    
    return {"message": "Analysis deleted successfully"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )