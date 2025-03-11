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

    # Check if the username or email already exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    try:
        # Create a new User object
        user = User(username=data.get('username'), email=data.get('email'))
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        
        # Login the User after signup (store user id in session)
        session['user_id'] = user.id  # Store user id in session
        session.permanent = True  # Make session permanent

    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        return jsonify({"error": "Failed to register user", "details": str(e)}), 500

    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')  # Get username from the request

    # Query the user by username
    user = User.query.filter_by(username=username).first()

    if user 
        session['user_id'] = user.id  # Store user id in session
        session.permanent = True  # Make session permanent
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
