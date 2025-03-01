from flask_sqlalchemy import SQLAlchemy
from app.extensions import db
from app.models.user import User
from app.models.category import Category

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.Enum('income', 'expense', name='transaction_type'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    user = db.relationship('User', back_populates='transactions') 
    category = db.relationship('Category', back_populates='transactions')

