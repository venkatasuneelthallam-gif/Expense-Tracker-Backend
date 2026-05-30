from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://venkatasuneelthallam_db_user:suneel076@cluster0.0daj34e.mongodb.net/?appName=Cluster0"
)

db = client["ExpenseTracker"]

expenses = db["expenses"]