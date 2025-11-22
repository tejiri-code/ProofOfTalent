# UK Global Talent Visa Analysis API

FastAPI backend for LLM-powered UK Global Talent visa application analysis.

## Features

- **Field Selection**: Choose from Digital Technology, Arts & Culture, or Science & Research
- **Interactive Questionnaire**: Field-specific questions to gather evidence
- **Document Upload**: Upload CV, recommendation letters, and portfolio items (PDF)
- **LLM Analysis**: GPT-4 powered evaluation against official visa criteria
- **Gap Analysis**: Identifies missing evidence and areas for improvement
- **Roadmap Generation**: Personalized action plan to strengthen application

## Installation

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Install ML dependencies (from parent directory):
```bash
cd ..
pip install -r ml/requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"  # Optional
```

## Running the Server

```bash
cd backend/app
python main.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at `http://localhost:8000`

## API Endpoints

### General
- `GET /` - API root and documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Fields
- `GET /api/fields` - Get available Global Talent visa fields

### Session Management
- `POST /api/session/create` - Create new analysis session
- `GET /api/session/{session_id}/status` - Get session status
- `DELETE /api/session/{session_id}` - Delete session

### Questionnaire
- `GET /api/questionnaire/{field}` - Get field-specific questionnaire
- `POST /api/session/{session_id}/questionnaire` - Save questionnaire responses

### Document Upload
- `POST /api/upload/{session_id}` - Upload PDF documents

### Analysis
- `POST /api/analyze/{session_id}` - Run LLM analysis
- `GET /api/results/{session_id}` - Get analysis results

## Example Usage

### 1. Create Session
```bash
curl -X POST "http://localhost:8000/api/session/create" \
  -H "Content-Type: application/json" \
  -d '{"field": "digital_technology"}'
```

### 2. Get Questionnaire
```bash
curl "http://localhost:8000/api/questionnaire/digital_technology"
```

### 3. Upload Documents
```bash
curl -X POST "http://localhost:8000/api/upload/{session_id}" \
  -F "files=@cv.pdf" \
  -F "files=@letter1.pdf" \
  -F "files=@letter2.pdf" \
  -F "files=@letter3.pdf"
```

### 4. Submit Questionnaire
```bash
curl -X POST "http://localhost:8000/api/session/{session_id}/questionnaire" \
  -H "Content-Type: application/json" \
  -d '{
    "years_experience": 7,
    "github_url": "https://github.com/username",
    "has_founded_company": true,
    "publications": 15
  }'
```

### 5. Run Analysis
```bash
curl -X POST "http://localhost:8000/api/analyze/{session_id}"
```

### 6. Get Results
```bash
curl "http://localhost:8000/api/results/{session_id}"
```

## Response Example

```json
{
  "session_id": "session_20241122_112500_a1b2c3d4",
  "status": "completed",
  "results": {
    "field": "digital_technology",
    "analysis": {
      "likelihood": 0.78,
      "assessment_level": "Exceptional Talent",
      "evidence_present": {
        "mandatory_documents": {
          "cv": "complete",
          "recommendation_letters": "complete",
          "portfolio_evidence": "strong"
        }
      },
      "gaps": [...],
      "strengths": [...],
      "overall_assessment": "..."
    },
    "roadmap": {
      "milestones": [...],
      "total_weeks": 12
    }
  }
}
```

## Directory Structure

```
backend/
├── app/
│   └── main.py          # FastAPI application
├── uploads/             # Uploaded documents (per session)
├── results/             # Analysis results (JSON files)
├── requirements.txt     # Backend dependencies
└── README.md           # This file
```

## Development

Access interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Notes

- Sessions are stored in memory (use Redis/database for production)
- Upload directory is automatically created
- PDF files only for document uploads
- Requires valid OPENAI_API_KEY for analysis

## Production Considerations

1. **Session Storage**: Replace in-memory sessions with Redis/database
2. **File Storage**: Use cloud storage (S3, GCS) for uploaded files
3. **Authentication**: Add API key/JWT authentication
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **CORS**: Configure appropriate CORS origins
6. **Logging**: Add comprehensive logging
7. **Error Handling**: Enhance error handling and validation
