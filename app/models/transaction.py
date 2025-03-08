from app.extensions import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum("received", "sent", name="transaction_type"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='transactions')

