from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.transaction import Transaction

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
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
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "category": t.category,
        "type": t.type,
        "date": t.date.strftime("%Y-%m-%d")
    } for t in transactions])

@transactions_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.get(id)

    if not transaction or transaction.user_id != user_id:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted"}), 200
