"""
MongoDB Database Configuration and Connection
Supports both local MongoDB and MongoDB Atlas (cloud)
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from typing import Optional
import os
from datetime import datetime
from bson import ObjectId
from urllib.parse import quote_plus
import certifi

# MongoDB Configuration
# For local MongoDB: mongodb://localhost:27017/
# For MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/
# For authenticated local: mongodb://username:password@localhost:27017/
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "proof_of_talent")

# Optional: Individual credentials (will construct URL if provided)
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost:27017")
MONGODB_AUTH_SOURCE = os.getenv("MONGODB_AUTH_SOURCE", "admin")

# Global MongoDB client
mongodb_client: Optional[AsyncIOMotorClient] = None


def get_database():
    """Get the database instance"""
    return mongodb_client[MONGODB_DATABASE]


async def connect_to_mongo():
    """Connect to MongoDB"""
    global mongodb_client
    try:
        # Use certifi certificates for SSL verification (required for Atlas)
        mongodb_client = AsyncIOMotorClient(
            MONGODB_URL,
            tlsCAFile=certifi.where()
        )
        # Verify connection
        await mongodb_client.admin.command('ping')
        print(f"✅ Connected to MongoDB at {MONGODB_URL}")
        
        # Create indexes
        await create_indexes()
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("✅ Closed MongoDB connection")


async def create_indexes():
    """Create database indexes for performance"""
    db = get_database()
    
    # CV Analyses collection indexes
    cv_analyses = db.cv_analyses
    await cv_analyses.create_index([("filename", ASCENDING)])
    await cv_analyses.create_index([("upload_date", DESCENDING)])
    await cv_analyses.create_index([("processing_status", ASCENDING)])
    await cv_analyses.create_index([("user_id", ASCENDING)])  # For multi-user support
    
    # Model Metrics collection indexes
    model_metrics = db.model_metrics
    await model_metrics.create_index([("visa_type", ASCENDING)])
    await model_metrics.create_index([("training_date", DESCENDING)])
    
    print("✅ Created database indexes")


# Helper functions for common operations
def serialize_doc(doc: dict) -> dict:
    """Convert MongoDB document to JSON-serializable dict"""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


def prepare_doc_for_insert(doc: dict) -> dict:
    """Prepare document for insertion"""
    if "id" in doc:
        del doc["id"]
    if "upload_date" not in doc:
        doc["upload_date"] = datetime.utcnow()
    return doc
