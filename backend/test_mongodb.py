"""
Test script to verify MongoDB connection and basic operations
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "proof_of_talent")


async def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    print("🔄 Testing MongoDB connection...")
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[MONGODB_DATABASE]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Test collections
        print("\n📊 Testing collections...")
        
        # Test cv_analyses collection
        cv_collection = db.cv_analyses
        test_doc = {
            "filename": "test_cv.pdf",
            "upload_date": datetime.utcnow(),
            "processing_status": "test",
            "features": {"test": True},
            "visa_analysis": {},
            "external_data": {}
        }
        
        result = await cv_collection.insert_one(test_doc)
        print(f"✅ Inserted test document with ID: {result.inserted_id}")
        
        # Retrieve the document
        retrieved = await cv_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Retrieved test document: {retrieved['filename']}")
        
        # Delete test document
        await cv_collection.delete_one({"_id": result.inserted_id})
        print(f"✅ Deleted test document")
        
        # Test model_metrics collection
        metrics_collection = db.model_metrics
        test_metric = {
            "visa_type": "test_visa",
            "auc_score": 0.95,
            "training_date": datetime.utcnow(),
            "feature_importances": {"feature1": 0.5}
        }
        
        result = await metrics_collection.insert_one(test_metric)
        print(f"✅ Inserted test metric with ID: {result.inserted_id}")
        
        await metrics_collection.delete_one({"_id": result.inserted_id})
        print(f"✅ Deleted test metric")
        
        # Show existing documents
        cv_count = await cv_collection.count_documents({})
        metrics_count = await metrics_collection.count_documents({})
        
        print(f"\n📈 Database Statistics:")
        print(f"   - CV Analyses: {cv_count} documents")
        print(f"   - Model Metrics: {metrics_count} documents")
        
        print("\n✅ All MongoDB tests passed!")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"\n❌ MongoDB test failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if MongoDB is running: brew services list")
        print("   2. Start MongoDB: brew services start mongodb-community")
        print("   3. Check connection string in .env file")
        return False
    
    return True


if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())
