import os
import sys
from pymongo import MongoClient

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://venkatasuneelthallam_db_user:suneel076@cluster0.0daj34e.mongodb.net/?appName=Cluster0"
)

print(f"DEBUG: Creating MongoDB client for: {MONGODB_URI[:50]}...", file=sys.stderr)

# Create the client but avoid blocking network operations at import time.
# Actual connectivity will be attempted lazily when the app performs DB ops.
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    db = client["ExpenseTracker"]
    expenses = db["expenses"]
    users = db["users"]
    print("DEBUG: MongoDB client created (connection deferred)", file=sys.stderr)
except Exception as e:
    print(f"ERROR: Failed to create MongoDB client: {str(e)}", file=sys.stderr)
    client = None
    db = None
    expenses = None
    users = None

