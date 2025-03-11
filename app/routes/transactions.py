from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.transaction import Transaction



transactions_bp = Blueprint('transactions', __name__)
main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/transactions', methods=['GET', 'POST'])
def transactions():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    if request.method == 'GET':
        # Handle GET request: Fetch all transactions for the logged-in user
        transactions = Transaction.query.filter_by(user_id=session['user_id']).all()
        transaction_list = [{
            'transaction_id': t.transaction_id,
            'user_id': t.user_id,  # Include user_id in the response (optional)
            'amount': t.amount,
            'date': t.date.isoformat(),
            'type': t.type
        } for t in transactions]

        return jsonify(transaction_list), 200

    elif request.method == 'POST':
        # Handle POST request: Add a new transaction
        data = request.get_json()

        # Validate required fields
        if not data or 'amount' not in data or 'date' not in data or 'type' not in data:
            return jsonify({'message': 'Missing required fields (amount, date, type)'}), 400

        try:
            # Parse the date from the frontend format (e.g., "4/16/2021, 7:41:15 PM")
            transaction_date = datetime.strptime(data['date'], '%m/%d/%Y, %I:%M:%S %p')
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use "MM/DD/YYYY, HH:MM:SS AM/PM"'}), 400

        # Create a new transaction
        new_transaction = Transaction(
            user_id=session['user_id'],  # Set the user_id from the session
            amount=data['amount'],
            date=transaction_date,
            type=data['type']
        )

        # Add and commit to the database
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({'message': 'Transaction added successfully', 'transaction_id': new_transaction.transaction_id}), 201
