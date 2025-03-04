Money-Mate Backend

Overview

Money-Mate is a finance tracking application that helps users manage their transactions, track expenses and income, and gain insights into their spending habits. This backend is built using Flask and SQLAlchemy, providing secure authentication, transaction management, and spending analytics.

Features

User Authentication: Secure user signup and login with password hashing.

Transaction Management: Record, categorize, and manage financial transactions.

Expense & Income Tracking: Users can track their earnings and expenditures.

Data Security: Passwords are stored securely, and authentication is token-based.

Database Integration: Uses SQLite for data persistence.

Technologies Used

Backend Framework: Flask

Database: SQLite with SQLAlchemy ORM

Authentication: JWT-based authentication

Environment Management: Python dotenv

Project Structure

.
├── app
│   ├── config.py         # Configuration settings
│   ├── extensions.py     # Database and migration initialization
│   ├── models            # Database models (User, Transaction, Category)
│   ├── routes            # API endpoints (Auth, Transactions, Analytics)
│   ├── services          # Additional services like alerts and analytics
├── app.py                # Main application entry point
├── instance              # Stores the SQLite database
├── migrations            # Alembic migrations for database schema updates
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation

Installation

Prerequisites

Python 3.8+

Virtual Environment (recommended)

Setup

Clone the repository:

git clone https://github.com/yourusername/Money-Mate-Backend.git
cd Money-Mate-Backend

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

cp .env.example .env

Edit .env and add necessary configurations like SECRET_KEY and DATABASE_URL.

Run database migrations:

flask db upgrade

Start the application:

flask run

The server will start at http://127.0.0.1:5000.

API Endpoints

Authentication

Method

Endpoint

Description

POST

/signup

Register a new user

POST

/login

Authenticate a user

Transactions

Method

Endpoint

Description

GET

/transactions

Retrieve all transactions

POST

/transactions

Create a new transaction

GET

/transactions/<id>

Get transaction by ID

DELETE

/transactions/<id>

Delete a transaction

Database Models

User Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

Transaction Model

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.DateTime, default=datetime.utcnow)

Contribution

Fork the repository

Create a feature branch (git checkout -b feature-name)

Commit changes (git commit -m 'Add new feature')

Push to the branch (git push origin feature-name)

Open a Pull Request

License

This project is licensed under the MIT License.