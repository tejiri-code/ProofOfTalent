"""
Test suite for CV Analysis API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import json

from main import app, Base, get_db

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixtures
@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def sample_pdf():
    """Create a sample PDF file for testing"""
    # You would need a real PDF file here
    pdf_path = Path("test_sample.pdf")
    if not pdf_path.exists():
        pytest.skip("Sample PDF not available")
    return pdf_path

# Test cases
def test_root_endpoint():
    """Test health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_health_endpoint():
    """Test detailed health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "models" in data

def test_upload_cv_invalid_file():
    """Test uploading non-PDF file"""
    files = {"file": ("test.txt", b"content", "text/plain")}
    response = client.post("/api/v1/analyze", files=files)
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]

def test_upload_cv_success(sample_pdf):
    """Test successful CV upload"""
    with open(sample_pdf, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        response = client.post("/api/v1/analyze", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["filename"] == "test.pdf"
    assert data["processing_status"] in ["processing", "completed"]

def test_get_analysis_not_found():
    """Test getting non-existent analysis"""
    response = client.get("/api/v1/analysis/999")
    assert response.status_code == 404

def test_get_analysis_success(sample_pdf):
    """Test retrieving analysis results"""
    # First upload a CV
    with open(sample_pdf, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        upload_response = client.post("/api/v1/analyze", files=files)
    
    analysis_id = upload_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/api/v1/analysis/{analysis_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == analysis_id

def test_list_analyses():
    """Test listing all analyses"""
    response = client.get("/api/v1/analyses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_analyses_with_filter():
    """Test listing with status filter"""
    response = client.get("/api/v1/analyses?status=completed")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_batch_upload(sample_pdf):
    """Test batch upload"""
    files = [
        ("files", ("test1.pdf", open(sample_pdf, "rb"), "application/pdf")),
        ("files", ("test2.pdf", open(sample_pdf, "rb"), "application/pdf")),
    ]
    
    response = client.post("/api/v1/batch-upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 0

def test_get_recommendations(sample_pdf):
    """Test getting visa recommendations"""
    # Upload and analyze
    with open(sample_pdf, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        upload_response = client.post("/api/v1/analyze", files=files)
    
    analysis_id = upload_response.json()["id"]
    
    # Get recommendations (might fail if processing not complete)
    response = client.get(f"/api/v1/recommendations/{analysis_id}")
    # Could be 200 or 400 depending on processing status
    assert response.status_code in [200, 400]

def test_compare_candidates():
    """Test candidate comparison"""
    request_data = {
        "candidate_ids": [1, 2],
        "visa_type": "uk_global_talent"
    }
    
    response = client.post("/api/v1/compare", json=request_data)
    # Will be 404 if no candidates exist
    assert response.status_code in [200, 404]

def test_get_model_metrics():
    """Test retrieving model metrics"""
    response = client.get("/api/v1/models/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data

def test_delete_analysis(sample_pdf):
    """Test deleting an analysis"""
    # Upload a CV
    with open(sample_pdf, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        upload_response = client.post("/api/v1/analyze", files=files)
    
    analysis_id = upload_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/v1/analysis/{analysis_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f"/api/v1/analysis/{analysis_id}")
    assert get_response.status_code == 404

def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers

# Integration tests
@pytest.mark.integration
def test_full_workflow(sample_pdf):
    """Test complete workflow from upload to recommendations"""
    # 1. Upload CV
    with open(sample_pdf, "rb") as f:
        files = {"file": ("integration_test.pdf", f, "application/pdf")}
        upload_response = client.post("/api/v1/analyze", files=files)
    
    assert upload_response.status_code == 200
    analysis_id = upload_response.json()["id"]
    
    # 2. Check status
    status_response = client.get(f"/api/v1/analysis/{analysis_id}")
    assert status_response.status_code == 200
    
    # 3. If processing complete, get recommendations
    if status_response.json()["processing_status"] == "completed":
        rec_response = client.get(f"/api/v1/recommendations/{analysis_id}")
        assert rec_response.status_code == 200
        recommendations = rec_response.json()
        assert len(recommendations) > 0
        assert all(0 <= r["likelihood"] <= 1 for r in recommendations)

# Performance tests
@pytest.mark.performance
def test_api_response_time():
    """Test API response times"""
    import time
    
    start = time.time()
    response = client.get("/health")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 1.0  # Should respond within 1 second

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])