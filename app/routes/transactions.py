from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.transaction import Transaction


transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['POST'])
def add_transaction():
    data = request.json

    # Check for required fields
    required_fields = ["amount", "type", "user_id"]
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    # validate the type field
    if data["type"] not in ["received", "sent"]:
        return jsonify({"error": "Invalid type field"}), 400

    # validate the amount field
    if not isinstance(data["amount"], (int, float)) or data["amount"] <= 0:
        return jsonify({"error": "Invalid amount field"}), 400


    # Create the Transaction instance
    transaction = Transaction(
        user_id=data["user_id"],  # Include the user_id from the request
        amount=data["amount"],
        type=data["type"]
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added"}), 201

@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    # Fetch all transactions (no user filtering since we're not using sessions)
    transactions = Transaction.query.all()

    # Return the transactions as a JSON response
    return jsonify([{
        "id": t.id,
        "user_id": t.user_id,  # Include user_id
        "amount": t.amount,
        "type": t.type,
        "date": t.date.strftime("%Y-%m-%d")
    } for t in transactions])

@transactions_bp.route('/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    # Fetch the transaction by ID
    transaction = Transaction.query.get(id)

    # Ensure the transaction exists
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    # Delete the transaction from the database
    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted"}), 200