"""
UK Global Talent Visa Analysis - FastAPI Backend
Uses the LLM-based analysis system from ml/model_combined.py
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import sys
import os
import json
import shutil
from datetime import datetime
from pydantic import BaseModel

# Add ml directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ml'))

from model_combined import (
    GLOBAL_TALENT_FIELDS,
    generate_evidence_questionnaire,
    analyze_global_talent_application,
    save_analysis_results
)

app = FastAPI(
    title="UK Global Talent Visa Analysis API",
    description="LLM-powered analysis for UK Global Talent visa applications",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directories
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Pydantic models for request/response
class FieldSelection(BaseModel):
    field: str

class QuestionnaireResponse(BaseModel):
    field: str
    responses: Dict[str, Any]

class AnalysisRequest(BaseModel):
    field: str
    questionnaire_responses: Dict[str, Any]
    session_id: str

# In-memory storage for sessions (use Redis/DB in production)
sessions = {}


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "UK Global Talent Visa Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "fields": "/api/fields",
            "questionnaire": "/api/questionnaire/{field}",
            "upload": "/api/upload/{session_id}",
            "analyze": "/api/analyze",
            "results": "/api/results/{session_id}"
        }
    }


@app.get("/api/fields")
async def get_fields():
    """Get available Global Talent visa fields"""
    return {
        "fields": [
            {"id": key, "name": value}
            for key, value in GLOBAL_TALENT_FIELDS.items()
        ]
    }


@app.get("/api/questionnaire/{field}")
async def get_questionnaire(field: str):
    """Get field-specific questionnaire"""
    if field not in GLOBAL_TALENT_FIELDS:
        raise HTTPException(status_code=400, detail="Invalid field")
    
    questions = generate_evidence_questionnaire(field)
    
    return {
        "field": field,
        "field_name": GLOBAL_TALENT_FIELDS[field],
        "questions": questions
    }


@app.post("/api/session/create")
async def create_session(field_selection: FieldSelection):
    """Create a new analysis session"""
    if field_selection.field not in GLOBAL_TALENT_FIELDS:
        raise HTTPException(status_code=400, detail="Invalid field")
    
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}"
    
    sessions[session_id] = {
        "field": field_selection.field,
        "created_at": datetime.now().isoformat(),
        "documents": [],
        "questionnaire_responses": {},
        "status": "created"
    }
    
    # Create session upload directory
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    return {
        "session_id": session_id,
        "field": field_selection.field,
        "field_name": GLOBAL_TALENT_FIELDS[field_selection.field]
    }


@app.post("/api/upload/{session_id}")
async def upload_documents(
    session_id: str,
    files: List[UploadFile] = File(...)
):
    """Upload evidence documents for analysis"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    uploaded_files = []
    
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail=f"Only PDF files allowed: {file.filename}")
        
        file_path = os.path.join(session_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        uploaded_files.append({
            "filename": file.filename,
            "path": file_path,
            "size": os.path.getsize(file_path)
        })
    
    sessions[session_id]["documents"].extend(uploaded_files)
    sessions[session_id]["status"] = "documents_uploaded"
    
    return {
        "session_id": session_id,
        "uploaded_files": len(uploaded_files),
        "total_documents": len(sessions[session_id]["documents"]),
        "files": [f["filename"] for f in uploaded_files]
    }


@app.post("/api/questionnaire/submit")
async def submit_questionnaire(response: QuestionnaireResponse):
    """Submit questionnaire responses (without session - for quick analysis)"""
    if response.field not in GLOBAL_TALENT_FIELDS:
        raise HTTPException(status_code=400, detail="Invalid field")
    
    return {
        "status": "success",
        "message": "Questionnaire responses received",
        "field": response.field,
        "responses_count": len(response.responses)
    }


@app.post("/api/session/{session_id}/questionnaire")
async def save_session_questionnaire(
    session_id: str,
    responses: Dict[str, Any]
):
    """Save questionnaire responses to session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sessions[session_id]["questionnaire_responses"] = responses
    sessions[session_id]["status"] = "questionnaire_completed"
    
    return {
        "session_id": session_id,
        "status": "success",
        "responses_saved": len(responses)
    }


@app.post("/api/analyze/{session_id}")
async def analyze_application(session_id: str):
    """Run LLM analysis on uploaded documents and questionnaire responses"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if not session["documents"]:
        raise HTTPException(status_code=400, detail="No documents uploaded")
    
    if not session["questionnaire_responses"]:
        raise HTTPException(status_code=400, detail="Questionnaire not completed")
    
    # Update status
    sessions[session_id]["status"] = "analyzing"
    
    try:
        # Get document paths
        document_paths = [doc["path"] for doc in session["documents"]]
        
        # Run analysis
        results = analyze_global_talent_application(
            field=session["field"],
            document_paths=document_paths,
            questionnaire_responses=session["questionnaire_responses"]
        )
        
        # Save results
        results_file = os.path.join(RESULTS_DIR, f"{session_id}_results.json")
        save_analysis_results(results, results_file)
        
        sessions[session_id]["results"] = results
        sessions[session_id]["results_file"] = results_file
        sessions[session_id]["status"] = "completed"
        sessions[session_id]["completed_at"] = datetime.now().isoformat()
        
        return {
            "session_id": session_id,
            "status": "completed",
            "results": results
        }
    
    except Exception as e:
        sessions[session_id]["status"] = "error"
        sessions[session_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/results/{session_id}")
async def get_results(session_id: str):
    """Get analysis results for a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if session["status"] != "completed":
        return {
            "session_id": session_id,
            "status": session["status"],
            "message": f"Analysis not yet completed. Current status: {session['status']}"
        }
    
    return {
        "session_id": session_id,
        "status": "completed",
        "results": session.get("results", {})
    }


@app.get("/api/session/{session_id}/status")
async def get_session_status(session_id: str):
    """Get current status of a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    return {
        "session_id": session_id,
        "status": session["status"],
        "field": session["field"],
        "created_at": session["created_at"],
        "documents_count": len(session["documents"]),
        "has_questionnaire": bool(session["questionnaire_responses"])
    }


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and its associated files"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete uploaded files
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
    
    # Delete results file
    if "results_file" in sessions[session_id]:
        results_file = sessions[session_id]["results_file"]
        if os.path.exists(results_file):
            os.remove(results_file)
    
    # Remove session
    del sessions[session_id]
    
    return {
        "status": "success",
        "message": f"Session {session_id} deleted"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
