# Dataset Generation & Dashboard Analytics - Implementation Guide

## Overview

I've updated the backend to save all analysis results to the `cv_analyses` MongoDB collection, enabling you to generate datasets and build dashboards.

---

## What Was Added

### 1. Automatic Data Collection

**File:** `/backend/app/main.py` - `run_analysis_task()` function

Every time an analysis completes, the system now saves a record to `cv_analyses` with:

```python
{
    "session_id": "session_20251123_...",
    "field": "digital_technology",  // or arts_culture, science_research
    "upload_date": "2025-11-23T15:00:00Z",
    "processing_status": "completed",
    "completed_at": "2025-11-23T15:05:00Z",
    "document_count": 3,
    "questionnaire_responses": {...},
    "analysis_results": {...},  // Full LLM analysis
    
    // Key metrics for easy querying
    "overall_score": 85,
    "likelihood": 0.75,
    "recommendation": "strong",
    "strengths_count": 12,
    "weaknesses_count": 3,
    "evidence_gaps_count": 2,
    
    "created_at": "2025-11-23T15:05:00Z"
}
```

### 2. Analytics API Endpoints

#### **GET /api/analytics/overview**
Get high-level statistics for your dashboard.

**Response:**
```json
{
    "total_analyses": 150,
    "completed": 145,
    "errors": 5,
    "success_rate": 96.67,
    "by_field": [
        {
            "_id": "digital_technology",
            "count": 80,
            "avg_score": 78.5,
            "avg_likelihood": 0.72
        },
        {
            "_id": "arts_culture",
            "count": 40,
            "avg_score": 82.3,
            "avg_likelihood": 0.78
        }
    ],
    "by_recommendation": [
        {"_id": "strong", "count": 60},
        {"_id": "moderate", "count": 50},
        {"_id": "weak", "count": 35}
    ],
    "recent_30_days": 45
}
```

**Use Cases:**
- Total analyses count
- Success rate percentage
- Distribution by field
- Distribution by recommendation
- Recent activity trends

---

#### **GET /api/analytics/analyses**
Get paginated list of all analyses with filtering.

**Parameters:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Number of results (default: 50, max: 50)
- `field` (string): Filter by field (optional)
- `status` (string): Filter by status (optional)

**Example:**
```bash
GET /api/analytics/analyses?skip=0&limit=20&field=digital_technology&status=completed
```

**Response:**
```json
{
    "analyses": [
        {
            "_id": "507f1f77bcf86cd799439011",
            "session_id": "session_20251123_150000_abc123",
            "field": "digital_technology",
            "overall_score": 85,
            "likelihood": 0.75,
            "recommendation": "strong",
            "created_at": "2025-11-23T15:00:00Z"
        },
        // ... more analyses
    ],
    "total": 150,
    "skip": 0,
    "limit": 20
}
```

**Use Cases:**
- Display analysis history
- Filter by field or status
- Paginate through results
- Show individual analysis details

---

#### **GET /api/analytics/export**
Export complete dataset for external analysis (Excel, Python, etc.)

**Response:**
```json
{
    "dataset": [
        {
            "_id": "507f1f77bcf86cd799439011",
            "session_id": "session_20251123_150000_abc123",
            "field": "digital_technology",
            "overall_score": 85,
            "likelihood": 0.75,
            "recommendation": "strong",
            "strengths_count": 12,
            "weaknesses_count": 3,
            "evidence_gaps_count": 2,
            "questionnaire_responses": {...},
            "analysis_results": {...},
            "created_at": "2025-11-23T15:00:00Z"
        },
        // ... all completed analyses
    ],
    "count": 145,
    "exported_at": "2025-11-23T15:30:00Z"
}
```

**Use Cases:**
- Export to CSV/Excel
- Machine learning training data
- Statistical analysis in Python/R
- Data visualization tools

---

## How to Use

### 1. Test the Endpoints

```bash
# Get overview statistics
curl https://proofoftalent.onrender.com/api/analytics/overview

# Get recent analyses
curl https://proofoftalent.onrender.com/api/analytics/analyses?limit=10

# Export full dataset
curl https://proofoftalent.onrender.com/api/analytics/export > dataset.json
```

### 2. Build a Dashboard

**Frontend Example (React/Next.js):**

```typescript
// Fetch analytics data
const response = await fetch('https://proofoftalent.onrender.com/api/analytics/overview');
const data = await response.json();

// Display in dashboard
<div>
  <h2>Total Analyses: {data.total_analyses}</h2>
  <p>Success Rate: {data.success_rate.toFixed(2)}%</p>
  
  <h3>By Field:</h3>
  {data.by_field.map(field => (
    <div key={field._id}>
      <p>{field._id}: {field.count} analyses</p>
      <p>Avg Score: {field.avg_score}</p>
    </div>
  ))}
</div>
```

### 3. Export to Excel

**Python Example:**

```python
import requests
import pandas as pd

# Fetch dataset
response = requests.get('https://proofoftalent.onrender.com/api/analytics/export')
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data['dataset'])

# Export to Excel
df.to_excel('global_talent_analyses.xlsx', index=False)

# Or CSV
df.to_csv('global_talent_analyses.csv', index=False)
```

### 4. MongoDB Queries

You can also query directly in MongoDB Atlas:

```javascript
// Find all strong recommendations
db.cv_analyses.find({
    "recommendation": "strong",
    "processing_status": "completed"
})

// Average score by field
db.cv_analyses.aggregate([
    { $match: { processing_status: "completed" } },
    { $group: {
        _id: "$field",
        avgScore: { $avg: "$overall_score" },
        count: { $sum: 1 }
    }}
])

// Recent analyses (last 7 days)
db.cv_analyses.find({
    created_at: {
        $gte: new Date(Date.now() - 7*24*60*60*1000)
    }
})
```

---

## Dashboard Ideas

### 1. **Overview Dashboard**
- Total analyses count
- Success rate gauge
- Analyses per field (pie chart)
- Recommendation distribution (bar chart)
- Trend over time (line chart)

### 2. **Field Comparison**
- Average scores by field
- Success rates by field
- Common strengths/weaknesses per field
- Evidence gaps analysis

### 3. **User Insights**
- Most common recommendations
- Average processing time
- Document upload patterns
- Questionnaire completion rates

### 4. **Quality Metrics**
- Error rate tracking
- Score distributions
- Likelihood distributions
- Strengths vs weaknesses ratio

---

## Data Collection

**When does data get saved?**
- ✅ Every time an analysis completes successfully
- ✅ When an analysis fails (with error tracking)
- ✅ Automatically in the background
- ✅ No user action required

**What data is collected?**
- ✅ Field selection
- ✅ Questionnaire responses
- ✅ Full LLM analysis results
- ✅ Extracted metrics (scores, recommendations)
- ✅ Timestamps and metadata

**Where is it stored?**
- ✅ MongoDB Atlas: `proof_of_talent.cv_analyses` collection
- ✅ Also in `sessions` collection (for session management)

---

## Next Steps

### 1. Run Some Analyses
Complete a few analyses through the frontend to populate the `cv_analyses` collection.

### 2. Check MongoDB
Go to MongoDB Atlas → `proof_of_talent` → `cv_analyses` and verify data is being saved.

### 3. Test Analytics Endpoints
Use the API endpoints to fetch data:
```bash
curl https://proofoftalent.onrender.com/api/analytics/overview
```

### 4. Build Your Dashboard
Options:
- **Simple:** Use Google Sheets + import JSON
- **Medium:** Build React dashboard with charts (Chart.js, Recharts)
- **Advanced:** Use Tableau, Power BI, or Metabase
- **Custom:** Build with Next.js + MongoDB Charts

### 5. Export Dataset
Download your data for analysis:
```bash
curl https://proofoftalent.onrender.com/api/analytics/export > my_dataset.json
```

---

## Troubleshooting

**Q: No data in cv_analyses collection?**
- Make sure you've completed at least one analysis after deploying this update
- Check backend logs for errors
- Verify MongoDB connection is working

**Q: Analytics endpoints returning empty data?**
- The collection might be empty (no analyses yet)
- Check if analyses are completing successfully
- Look for errors in the backend logs

**Q: How to reset/clear data?**
- In MongoDB Atlas, you can delete documents from `cv_analyses`
- Or use: `db.cv_analyses.deleteMany({})`

---

## Summary

✅ **Data Collection:** Automatic on every analysis  
✅ **Storage:** MongoDB `cv_analyses` collection  
✅ **Analytics API:** 3 endpoints for dashboard data  
✅ **Export:** Full dataset export capability  
✅ **Ready to Use:** Deploy and start collecting data!

Your backend is now ready to generate datasets and power dashboards! 🎉
