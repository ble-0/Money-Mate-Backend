
from flask import request, jsonify
from app import app, db
from app.models import User, Transaction
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
from sqlalchemy.exc import SQLAlchemyError

# Helper function to validate email
def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email)

# Helper function to validate password strength
def is_strong_password(password):
    password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password)

# User Registration (Sign-up)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check for missing fields
    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    # Validate email format
    if not is_valid_email(email):
        return jsonify({"msg": "Invalid email format"}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    # Validate password strength
    if not is_strong_password(password):
        return jsonify({"msg": "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password, method='sha256')

    # Create the new user
    new_user = User(username=username, email=email, password_hash=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error creating user", "error": str(e)}), 500

    # Optionally return user info (excluding password)
    return jsonify({
        "msg": "User created successfully",
        "username": new_user.username,
        "email": new_user.email
    }), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "Email not found"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Incorrect password"}), 401

    # Generate the access token
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Add a Transaction
@app.route('/transactions', methods=['POST'])
@jwt_required()
def add_transaction():
    data = request.get_json()

    # Validate input data
    amount = data.get('amount')
    category = data.get('category')
    transaction_type = data.get('type')

    if not amount or not category or not transaction_type:
        return jsonify({"msg": "Missing required fields"}), 400
    
    # Example validation: amount should be a positive number
    if amount <= 0:
        return jsonify({"msg": "Amount must be positive"}), 400

    user_id = get_jwt_identity()

    # Create a new transaction
    new_transaction = Transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        type=transaction_type,
        date=datetime.utcnow()  # Set the transaction date to the current UTC time
    )

    try:
        db.session.add(new_transaction)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"msg": "Failed to add transaction"}), 500

    return jsonify({"msg": "Transaction added successfully"}), 201

# Get User's Transactions
@app.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    # Build response data
    transaction_list = [{"amount": t.amount, "category": t.category, "type": t.type, "date": t.date} for t in transactions]
    
    return jsonify(transaction_list), 200

# Edit a Transaction
@app.route('/transactions/<int:id>', methods=['PUT'])
@jwt_required()
def edit_transaction(id):
    data = request.get_json()
    transaction = Transaction.query.get_or_404(id)

    if transaction.user_id != get_jwt_identity():
        return jsonify({"msg": "Unauthorized"}), 403

    # Validate input data
    amount = data.get('amount', transaction.amount)
    category = data.get('category', transaction.category)
    transaction_type = data.get('type', transaction.type)

    if not amount or not category or not transaction_type:
        return jsonify({"msg": "Missing required fields"}), 400
    
    if amount <= 0:
        return jsonify({"msg": "Amount must be positive"}), 400

    # Update the transaction
    transaction.amount = amount
    transaction.category = category
    transaction.type = transaction_type

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"msg": "Failed to update transaction"}), 500

    return jsonify({"msg": "Transaction updated successfully"}), 200

# Delete a Transaction
@app.route('/transactions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if transaction.user_id != get_jwt_identity():
        return jsonify({"msg": "Unauthorized"}), 403

    try:
        db.session.delete(transaction)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"msg": "Failed to delete transaction"}), 500

    return jsonify({"msg": "Transaction deleted successfully"}), 200
