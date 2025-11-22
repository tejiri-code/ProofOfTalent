"""
Quick test script for MongoDB Atlas connection
Tests the connection with the provided credentials
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import certifi

# MongoDB Atlas connection string
MONGODB_URL = "mongodb+srv://evelynedjere_db_user:AQOADjJfYVQE19dV@proofoftalent.pkhflyz.mongodb.net/?appName=ProofOfTalent"
MONGODB_DATABASE = "proof_of_talent"


async def test_atlas_connection():
    """Test MongoDB Atlas connection"""
    print("🔄 Testing MongoDB Atlas connection...")
    print(f"📍 Cluster: proofoftalent.pkhflyz.mongodb.net")
    print(f"👤 User: evelynedjere_db_user")
    print(f"🗄️  Database: {MONGODB_DATABASE}\n")
    
    try:
        # Connect to MongoDB Atlas with proper SSL certificate handling
        client = AsyncIOMotorClient(
            MONGODB_URL,
            tlsCAFile=certifi.where()  # Use certifi's certificate bundle
        )
        db = client[MONGODB_DATABASE]
        
        # Test connection with ping
        result = await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Get server info
        server_info = await client.server_info()
        print(f"✅ MongoDB version: {server_info.get('version')}")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"✅ Existing collections: {collections if collections else 'None (new database)'}")
        
        # Test write operation
        print("\n📝 Testing write operation...")
        cv_collection = db.cv_analyses
        test_doc = {
            "filename": "test_connection.pdf",
            "upload_date": datetime.utcnow(),
            "processing_status": "test",
            "test": True
        }
        
        result = await cv_collection.insert_one(test_doc)
        print(f"✅ Insert successful! Document ID: {result.inserted_id}")
        
        # Test read operation
        print("📖 Testing read operation...")
        retrieved = await cv_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Read successful! Document: {retrieved['filename']}")
        
        # Clean up test document
        await cv_collection.delete_one({"_id": result.inserted_id})
        print(f"🗑️  Cleaned up test document")
        
        # Show database stats
        stats = await db.command("dbStats")
        print(f"\n📊 Database Statistics:")
        print(f"   - Collections: {stats.get('collections', 0)}")
        print(f"   - Data Size: {stats.get('dataSize', 0)} bytes")
        print(f"   - Storage Size: {stats.get('storageSize', 0)} bytes")
        
        print("\n✅ All tests passed! MongoDB Atlas is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Copy .env.production to .env")
        print("   2. Run: python main_mongodb.py")
        
        # Close connection
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your internet connection")
        print("   2. Verify the username and password are correct")
        print("   3. Check MongoDB Atlas network access settings")
        print("   4. Ensure your IP address is whitelisted in Atlas")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_atlas_connection())
    exit(0 if success else 1)
