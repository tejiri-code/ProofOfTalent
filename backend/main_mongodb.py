"""
FastAPI Backend for CV Analysis System with MongoDB
Main application entry point
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
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
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Database
from database import (
    connect_to_mongo, close_mongo_connection, get_database, 
    serialize_doc, prepare_doc_for_insert
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CV Analysis API",
    description="Multi-domain CV analysis with visa eligibility prediction - MongoDB Edition",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[" *"],
)

# Global model storage and configuration
MODELS = {}
UPLOAD_DIR = Path("uploaded_cvs")
UPLOAD_DIR.mkdir(exist_ok=True)

# Pydantic models for API
class AnalysisResponse(BaseModel):
    id: str
    filename: str
    processing_status: str
    upload_date: datetime
    features: Optional[Dict[str, Any]] = None
    visa_analysis: Optional[Dict[str, Any]] = None
    external_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
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
    candidate_ids: List[str]
    visa_type: str = "uk_global_talent"

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection and models on startup"""
    logger.info("Starting up CV Analysis API with MongoDB...")
    
    try:
        # Connect to MongoDB
        await connect_to_mongo()
        
        # Initialize ML models (placeholder - implement based on your cv_analyzer)
        logger.info("Initializing ML models...")
        global MODELS
        # TODO: Implement model training
        # MODELS = await train_visa_models()
        logger.info("✅ Startup complete")
        
        # Save initial model metrics to MongoDB
        db = get_database()
        model_metrics = db.model_metrics
        
        # Example: Save model metrics
        # for visa, model_info in MODELS.items():
        #     await model_metrics.insert_one({
        #         "visa_type": visa,
        #         "auc_score": model_info.get('auc', 0.0),
        #         "training_date": datetime.utcnow(),
        #         "feature_importances": model_info.get('feature_importances', {})
        #     })
            
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()

# Health check endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CV Analysis API (MongoDB)",
        "version": "2.0.0",
        "models_loaded": len(MODELS),
        "database": "MongoDB"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    db = get_database()
    
    try:
        # Test MongoDB connection
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
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
    background_tasks: BackgroundTasks = None
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
    
    # Create database record in MongoDB
    db = get_database()
    cv_collection = db.cv_analyses
    
    analysis_doc = {
        "filename": file.filename,
        "upload_date": datetime.utcnow(),
        "processing_status": "processing",
        "features": {},
        "visa_analysis": {},
        "external_data": {},
        "file_path": str(file_path),
        "error_message": None
    }
    
    result = await cv_collection.insert_one(analysis_doc)
    analysis_id = str(result.inserted_id)
    
    # Process CV in background
    if background_tasks:
        background_tasks.add_task(process_cv_task, analysis_id, str(file_path))
    else:
        # Process synchronously if no background tasks
        await process_cv_sync(analysis_id, str(file_path))
    
    analysis_doc["id"] = analysis_id
    return AnalysisResponse(**analysis_doc)

async def process_cv_sync(analysis_id: str, file_path: str):
    """Process CV synchronously"""
    db = get_database()
    cv_collection = db.cv_analyses
    
    try:
        # TODO: Implement CV parsing and analysis
        # This is a placeholder - implement based on your cv_analyzer module
        # text = parse_pdf_cv(file_path)
        # parsed = parse_cv(text)
        # result = analyze_candidate_comprehensive(parsed, MODELS)
        
        # Placeholder result
        result = {
            "features": {
                "years_experience": 0,
                "total_skills": 0,
                "education_level": "unknown"
            },
            "visa_analysis": {},
            "external_data": {}
        }
        
        # Update database
        await cv_collection.update_one(
            {"_id": ObjectId(analysis_id)},
            {"$set": {
                "features": result.get('features', {}),
                "visa_analysis": result.get('visa_analysis', {}),
                "external_data": result.get('external_data', {}),
                "processing_status": "completed"
            }}
        )
        
    except Exception as e:
        logger.error(f"Error processing CV {analysis_id}: {e}")
        await cv_collection.update_one(
            {"_id": ObjectId(analysis_id)},
            {"$set": {
                "processing_status": "failed",
                "error_message": str(e)
            }}
        )

async def process_cv_task(analysis_id: str, file_path: str):
    """Background task for CV processing"""
    await process_cv_sync(analysis_id, file_path)

@app.post("/api/v1/batch-upload", response_model=BatchUploadResponse)
async def batch_upload(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload multiple CVs for batch processing
    """
    uploaded = []
    db = get_database()
    cv_collection = db.cv_analyses
    
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            continue
            
        file_path = UPLOAD_DIR / file.filename
        try:
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Create database record
            analysis_doc = {
                "filename": file.filename,
                "upload_date": datetime.utcnow(),
                "processing_status": "processing",
                "file_path": str(file_path)
            }
            
            result = await cv_collection.insert_one(analysis_doc)
            analysis_id = str(result.inserted_id)
            
            # Queue for processing
            if background_tasks:
                background_tasks.add_task(process_cv_task, analysis_id, str(file_path))
            
            uploaded.append(file.filename)
            
        except Exception as e:
            logger.error(f"Error uploading {file.filename}: {e}")
    
    return BatchUploadResponse(
        uploaded_files=uploaded,
        total_count=len(uploaded),
        message=f"Successfully queued {len(uploaded)} CVs for processing"
    )

@app.get("/api/v1/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    """
    Get analysis results by ID
    """
    db = get_database()
    cv_collection = db.cv_analyses
    
    try:
        analysis = await cv_collection.find_one({"_id": ObjectId(analysis_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid analysis ID format")
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis = serialize_doc(analysis)
    return AnalysisResponse(**analysis)

@app.get("/api/v1/analyses", response_model=List[AnalysisResponse])
async def list_analyses(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
):
    """
    List all analyses with optional filtering
    """
    db = get_database()
    cv_collection = db.cv_analyses
    
    # Build query filter
    query = {}
    if status:
        query["processing_status"] = status
    
    # Fetch analyses
    cursor = cv_collection.find(query).sort("upload_date", -1).skip(skip).limit(limit)
    analyses = await cursor.to_list(length=limit)
    
    return [AnalysisResponse(**serialize_doc(a)) for a in analyses]

@app.get("/api/v1/recommendations/{analysis_id}", response_model=List[VisaRecommendation])
async def get_recommendations(analysis_id: str):
    """
    Get visa recommendations sorted by likelihood
    """
    db = get_database()
    cv_collection = db.cv_analyses
    
    try:
        analysis = await cv_collection.find_one({"_id": ObjectId(analysis_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid analysis ID format")
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if not analysis.get('visa_analysis'):
        raise HTTPException(status_code=400, detail="Analysis not yet completed")
    
    recommendations = []
    for visa, data in analysis['visa_analysis'].items():
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
async def compare_candidates(request: ComparisonRequest):
    """
    Compare multiple candidates for a specific visa
    """
    db = get_database()
    cv_collection = db.cv_analyses
    
    # Convert string IDs to ObjectId
    try:
        object_ids = [ObjectId(id) for id in request.candidate_ids]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid candidate ID format")
    
    analyses = await cv_collection.find({"_id": {"$in": object_ids}}).to_list(length=100)
    
    if not analyses:
        raise HTTPException(status_code=404, detail="No analyses found")
    
    comparison = []
    for analysis in analyses:
        if not analysis.get('visa_analysis'):
            continue
            
        visa_data = analysis['visa_analysis'].get(request.visa_type, {})
        comparison.append({
            'id': str(analysis['_id']),
            'filename': analysis['filename'],
            'likelihood': visa_data.get('likelihood', 0),
            'experience': analysis.get('features', {}).get('years_experience', 0),
            'skills': analysis.get('features', {}).get('total_skills', 0),
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
async def get_model_metrics():
    """
    Get current model performance metrics
    """
    db = get_database()
    model_metrics = db.model_metrics
    
    cursor = model_metrics.find().sort("training_date", -1).limit(10)
    metrics = await cursor.to_list(length=10)
    
    return {
        'models': [
            {
                'visa_type': m.get('visa_type'),
                'auc_score': m.get('auc_score'),
                'training_date': m.get('training_date').isoformat() if m.get('training_date') else None,
                'feature_importances': m.get('feature_importances', {})
            }
            for m in metrics
        ]
    }

@app.delete("/api/v1/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """
    Delete an analysis record
    """
    db = get_database()
    cv_collection = db.cv_analyses
    
    try:
        analysis = await cv_collection.find_one({"_id": ObjectId(analysis_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid analysis ID format")
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Delete file if exists
    file_path = Path(analysis.get('file_path', ''))
    if file_path.exists():
        file_path.unlink()
    
    await cv_collection.delete_one({"_id": ObjectId(analysis_id)})
    
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
