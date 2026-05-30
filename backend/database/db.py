import os
from pymongo import MongoClient

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://venkatasuneelthallam_db_user:suneel076@cluster0.0daj34e.mongodb.net/?appName=Cluster0"
)

client = MongoClient(MONGODB_URI)

db = client["ExpenseTracker"]

expenses = db["expenses"]
users = db["users"]
