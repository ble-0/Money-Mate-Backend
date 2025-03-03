from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        user_id=data['user_id'],
        amount=data['amount'],
        category=data['category'],
        type=data['type']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added"}), 201

@transactions_bp.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": t.id, "amount": t.amount, "category": t.category, "type": t.type, "date": t.date
    } for t in transactions]), 200

