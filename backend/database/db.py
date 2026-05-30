import os
import sys
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://venkatasuneelthallam_db_user:suneel076@cluster0.0daj34e.mongodb.net/?appName=Cluster0"
)

print(f"DEBUG: Attempting to connect to MongoDB at: {MONGODB_URI[:50]}...", file=sys.stderr)

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ping')
    print("DEBUG: MongoDB connection successful", file=sys.stderr)
except ServerSelectionTimeoutError as e:
    print(f"ERROR: MongoDB connection failed: {str(e)}", file=sys.stderr)
    client = None
except Exception as e:
    print(f"ERROR: Unexpected MongoDB error: {str(e)}", file=sys.stderr)
    client = None

try:
    if client:
        db = client["ExpenseTracker"]
        expenses = db["expenses"]
        users = db["users"]
    else:
        raise Exception("MongoDB client is not available")
        db = None
        expenses = None
        users = None
except Exception as e:
    print(f"ERROR: Failed to initialize database: {str(e)}", file=sys.stderr)
    db = None
    expenses = None
    users = None

