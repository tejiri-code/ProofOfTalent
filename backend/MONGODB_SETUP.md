# MongoDB Integration Setup

## Overview
The CV Analysis system now uses MongoDB for document storage instead of SQLite/PostgreSQL.

## Prerequisites

1. **Install MongoDB**:
   ```bash
   # macOS (using Homebrew)
   brew tap mongodb/brew
   brew install mongodb-community
   
   # Start MongoDB
   brew services start mongodb-community
   
   # Or run manually
   mongod --config /usr/local/etc/mongod.conf
   ```

2. **Verify MongoDB is running**:
   ```bash
   # Check if MongoDB is running
   brew services list | grep mongodb
   
   # Connect to MongoDB shell
   mongosh
   ```

## Setup Instructions

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.mongodb.example .env
   
   # Edit .env and update MongoDB connection string if needed
   # For local MongoDB: mongodb://localhost:27017/
   # For MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/
   ```

3. **Run the application**:
   ```bash
   # Use the new MongoDB-based main file
   python main_mongodb.py
   ```

## MongoDB Collections

The application creates the following collections:

### `cv_analyses`
Stores CV upload and analysis data:
```json
{
  "_id": ObjectId,
  "filename": "string",
  "upload_date": "ISODate",
  "processing_status": "pending|processing|completed|failed",
  "features": {},
  "visa_analysis": {},
  "external_data": {},
  "file_path": "string",
  "error_message": "string|null"
}
```

### `model_metrics`
Stores ML model performance metrics:
```json
{
  "_id": ObjectId,
  "visa_type": "string",
  "auc_score": "float",
  "training_date": "ISODate",
  "feature_importances": {}
}
```

## Database Indexes

The following indexes are created automatically on startup:
- `cv_analyses.filename` (ascending)
- `cv_analyses.upload_date` (descending)
- `cv_analyses.processing_status` (ascending)
- `cv_analyses.user_id` (ascending) - for future multi-user support
- `model_metrics.visa_type` (ascending)
- `model_metrics.training_date` (descending)

## Viewing Data

### Using MongoDB Compass (GUI)
1. Download from: https://www.mongodb.com/products/compass
2. Connect to: `mongodb://localhost:27017/`
3. Select database: `proof_of_talent`

### Using MongoDB Shell
```bash
# Connect to MongoDB
mongosh

# Switch to database
use proof_of_talent

# View all CV analyses
db.cv_analyses.find().pretty()

# Count documents
db.cv_analyses.countDocuments()

# Find by status
db.cv_analyses.find({ processing_status: "completed" })
```

## Migration from SQLite

If you have existing data in SQLite and want to migrate:

1. Export data from SQLite (create a migration script)
2. Transform to MongoDB document format
3. Import using MongoDB tools or Python script

## Backup and Restore

### Backup
```bash
# Backup entire database
mongodump --db=proof_of_talent --out=/path/to/backup

# Backup specific collection
mongodump --db=proof_of_talent --collection=cv_analyses --out=/path/to/backup
```

### Restore
```bash
# Restore entire database
mongorestore --db=proof_of_talent /path/to/backup/proof_of_talent

# Restore specific collection
mongorestore --db=proof_of_talent --collection=cv_analyses /path/to/backup/proof_of_talent/cv_analyses.bson
```

## API Changes

All API endpoints remain the same, but:
- Document IDs are now MongoDB ObjectIds (24-character hex strings)
- Responses use `id` field instead of numeric IDs
- All operations are async using Motor driver

## Troubleshooting

### MongoDB not connecting
- Check if MongoDB is running: `brew services list`
- Check connection string in `.env`
- Check MongoDB logs: `tail -f /usr/local/var/log/mongodb/mongo.log`

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+recommended)

### Performance issues
- Check indexes are created: `db.cv_analyses.getIndexes()`
- Monitor queries: Enable MongoDB profiling
