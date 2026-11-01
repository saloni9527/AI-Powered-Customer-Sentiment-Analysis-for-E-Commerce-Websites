"""
MongoDB Atlas Connection Test Script
Run this to verify your MongoDB setup is working correctly.
"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Load environment variables from .env file
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    
    MONGO_URI = os.environ.get("MONGO_URI")
    
    print("=" * 60)
    print("MongoDB Atlas Connection Test")
    print("=" * 60)
    
    # Check if MONGO_URI is set
    if not MONGO_URI:
        print("❌ ERROR: MONGO_URI not found in .env file")
        print("\nTo fix:")
        print("1. Copy .env.example to .env")
        print("2. Add your MongoDB Atlas connection string to MONGO_URI")
        return False
    
    print(f"\n📍 Testing connection to MongoDB Atlas...")
    print(f"URI: {MONGO_URI[:50]}..." if len(MONGO_URI) > 50 else f"URI: {MONGO_URI}")
    
    try:
        # Create client with timeout
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Ping the server
        print("\n🔍 Pinging MongoDB server...")
        mongo_client.admin.command('ping')
        print("✅ Server ping successful!")
        
        # Access the database
        print("\n🔍 Accessing 'sentiment_analyzer' database...")
        db = mongo_client.sentiment_analyzer
        print("✅ Database accessed successfully!")
        
        # List collections
        print("\n🔍 Collections found:")
        collections = db.list_collection_names()
        if collections:
            for collection in collections:
                count = db[collection].count_documents({})
                print(f"   • {collection}: {count} documents")
        else:
            print("   (No collections yet - will be created when you add users)")
        
        # Try to access users collection
        print("\n🔍 Checking 'users' collection...")
        users_count = db.users.count_documents({})
        print(f"✅ Users collection accessible: {users_count} user(s) found")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed! MongoDB is correctly configured.")
        print("=" * 60)
        
        print("\n📝 Next steps:")
        print("1. Start your Flask app: python app.py")
        print("2. Go to http://localhost:5000/auth/signup")
        print("3. Create a test account")
        print("4. Login and verify it works")
        
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"\n❌ Connection Failed: {str(e)}")
        print("\n🔧 Troubleshooting steps:")
        print("1. ✓ Verify your MongoDB URI is correct in .env")
        print("2. ✓ Check username and password (not account credentials)")
        print("3. ✓ Add your IP to MongoDB Atlas Network Access:")
        print("     - Go to Security > Network Access")
        print("     - Click 'Add IP Address'")
        print("     - Select 'Allow access from anywhere' (0.0.0.0/0)")
        print("4. ✓ Verify cluster name matches URI")
        print("5. ✓ Check internet connection")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {type(e).__name__}: {str(e)}")
        print("\n💡 Common issues:")
        print("   • Invalid connection string format")
        print("   • Database user doesn't exist")
        print("   • Special characters in password not properly encoded")
        return False
        
    finally:
        try:
            mongo_client.close()
            print("\n🔌 Connection closed.")
        except:
            pass


if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
