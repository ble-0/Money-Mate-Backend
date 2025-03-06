from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.transaction import Transaction

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['POST'])
def add_transaction():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    if not all(k in data for k in ["amount", "category", "type"]):
        return jsonify({"error": "Missing fields"}), 400

    transaction = Transaction(
        user_id=user_id,
        amount=data["amount"],
        category=data["category"],
        type=data["type"]
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added"}), 201

@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "category": t.category,
        "type": t.type,
        "date": t.date.strftime("%Y-%m-%d")
    } for t in transactions])

@transactions_bp.route('/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    transaction = Transaction.query.get(id)

    if not transaction or transaction.user_id != user_id:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted"}), 200
