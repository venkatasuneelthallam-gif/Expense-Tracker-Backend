from datetime import datetime
from flask import Blueprint, request, jsonify
from database.db import expenses, users
from bson import ObjectId
from models.expense import Expense

expense_bp = Blueprint("expense_bp", __name__)


def _get_user_email():
    email = None
    if request.args.get("email"):
        email = request.args.get("email")
    elif request.headers.get("X-User-Email"):
        email = request.headers.get("X-User-Email")
    elif request.json:
        email = request.json.get("user_email")
    return email.lower() if email else None


@expense_bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.json or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"message": "Please provide name, email and password."}), 400

    if users.find_one({"email": email}):
        return jsonify({"message": "Email already registered."}), 409

    user = {
        "name": name,
        "email": email,
        "password": password,
        "joined": datetime.utcnow().strftime("%Y-%m-%d")
    }

    users.insert_one(user)

    return jsonify({
        "message": "Account created successfully.",
        "user": {
            "name": name,
            "email": email,
            "joined": user["joined"]
        }
    })


@expense_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.json or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    user = users.find_one({"email": email, "password": password})
    if not user:
        return jsonify({"message": "Invalid login credentials."}), 401

    return jsonify({
        "message": "Login successful.",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "joined": user["joined"]
        }
    })


@expense_bp.route("/expenses", methods=["GET"])
def get_expenses():
    email = _get_user_email()
    if not email:
        return jsonify({"message": "User email is required."}), 400

    data = []
    query = {"user_email": email}
    for expense in expenses.find(query):
        expense["_id"] = str(expense["_id"])
        data.append(expense)

    return jsonify(data)


@expense_bp.route("/expenses", methods=["POST"])
def add_expense():
    data = request.json or {}
    data["user_email"] = _get_user_email() or data.get("user_email")

    if not Expense.validate(data):
        return jsonify({"message": "Please provide title, amount, category, date, and user_email."}), 400

    expense = Expense(
        title=data["title"],
        amount=data["amount"],
        category=data["category"],
        date=data["date"],
        user_email=data["user_email"]
    )

    result = expenses.insert_one(expense.to_dict())

    return jsonify({
        "message": "Expense Added",
        "id": str(result.inserted_id)
    })


@expense_bp.route("/expenses/<id>", methods=["PUT"])
def update_expense(id):
    email = _get_user_email()
    data = request.json or {}

    if not email:
        return jsonify({"message": "User email is required."}), 400

    result = expenses.update_one(
        {"_id": ObjectId(id), "user_email": email},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Expense not found or access denied."}), 404

    return jsonify({"message": "Expense Updated"})


@expense_bp.route("/expenses/<id>", methods=["DELETE"])
def delete_expense(id):
    email = _get_user_email()
    if not email:
        return jsonify({"message": "User email is required."}), 400

    result = expenses.delete_one(
        {"_id": ObjectId(id), "user_email": email}
    )

    if result.deleted_count == 0:
        return jsonify({"message": "Expense not found or access denied."}), 404

    return jsonify({"message": "Expense Deleted"})


@expense_bp.route("/report", methods=["GET"])
def report():
    email = _get_user_email()
    match_stage = {"$match": {"user_email": email}} if email else {"$match": {}}

    pipeline = [
        match_stage,
        {
            "$group": {
                "_id": "$category",
                "total": {
                    "$sum": "$amount"
                }
            }
        }
    ]

    result = list(expenses.aggregate(pipeline))

    return jsonify(result)
