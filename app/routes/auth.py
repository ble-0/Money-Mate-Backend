from flask import Blueprint, request, jsonify, session
from flask_session import Session
from datetime import datetime
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not all(k in data for k in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409



    try:
        # Create a new User object
        user = User(username=data.get('username'), email=data.get('email'))
        user.set_password(data["password"])  # hash the password
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        return jsonify({"error": "Failed to register user", "details": str(e)}), 500

    # # # Login the User after signup
    # session['user_id'] = user.id
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST','GET'])
# 
def login():
    data = request.get_json()

    username = data.get('username')  # Get username from the request
    password = data.get('password')  # Get password from the request

    user = User.query.filter_by(username=data.get("username")).first()
    
    # Check if the user exists and the password is correct
    if user and user.check_password(password):
        # Store the user's ID in the session
        session['user_id'] = user.user_id
        session.permanent = True  # Make the session permanent
        return jsonify({'success': True, 'message': 'Login successful'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    # Log the user out by clearing the session and marking them as not logged in
    user = User.query.get(user_id)
    user.logged_in = False  # Set the logged_in flag to False
    db.session.commit()
    
    session.clear()# clear the session
    session.modified = True
    response = jsonify({"message": "Logged out successfully"})

    return response, 200

@auth_bp.route('/check_auth', methods=['GET'])
def check_auth():
    user_id = session.get('user_id')
    print("Session in check_auth:", session)  # Debugging: Print the session
    print("User ID in session:", user_id)  

    if user_id:
        user = User.query.get(user_id)
        return jsonify({
            "message": "User is authenticated",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200
    return jsonify({"message": "User is not authenticated"}), 401
