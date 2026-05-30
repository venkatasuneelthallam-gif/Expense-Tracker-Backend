from flask import Blueprint, request, jsonify
from database.db import expenses
from bson import ObjectId
from models.expense import Expense
expense_bp = Blueprint("expense_bp", __name__)

# GET ALL EXPENSES
@expense_bp.route("/expenses", methods=["GET"])
def get_expenses():

    data = []

    for expense in expenses.find():

        expense["_id"] = str(expense["_id"])

        data.append(expense)

    return jsonify(data)

#add expenses
@expense_bp.route("/expenses", methods=["POST"])
def add_expense():

    data = request.json

    expense = Expense(
        title=data["title"],
        amount=data["amount"],
        category=data["category"],
        date=data["date"]
    )

    result = expenses.insert_one(expense.to_dict())

    return jsonify({
        "message": "Expense Added",
        "id": str(result.inserted_id)
    })


# UPDATE EXPENSE
@expense_bp.route("/expenses/<id>", methods=["PUT"])
def update_expense(id):

    data = request.json

    expenses.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )

    return jsonify({
        "message": "Expense Updated"
    })


# DELETE EXPENSE
@expense_bp.route("/expenses/<id>", methods=["DELETE"])
def delete_expense(id):

    expenses.delete_one(
        {"_id": ObjectId(id)}
    )

    return jsonify({
        "message": "Expense Deleted"
    })
@expense_bp.route("/report", methods=["GET"])
def report():

    pipeline = [
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