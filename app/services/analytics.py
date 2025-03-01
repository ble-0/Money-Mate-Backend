from app.models.transaction import Transaction
from app.extensions import db
from datetime import datetime, timedelta

def get_total_income_expense(user_id):
    """Calculate total income and expenses for a user."""
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id, Transaction.transaction_type == 'income'
    ).scalar() or 0

    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id, Transaction.transaction_type == 'expense'
    ).scalar() or 0

    return {"total_income": total_income, "total_expense": total_expense}

def get_transaction_summary(user_id, period="monthly"):
    """Get transaction summaries (daily, weekly, monthly)."""
    if period == "daily":
        start_date = datetime.utcnow() - timedelta(days=1)
    elif period == "weekly":
        start_date = datetime.utcnow() - timedelta(weeks=1)
    else:  # Default to monthly
        start_date = datetime.utcnow() - timedelta(days=30)

    summary = db.session.query(
        db.func.date(Transaction.timestamp).label("date"),
        db.func.sum(Transaction.amount).label("total_amount"),
        Transaction.transaction_type
    ).filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= start_date
    ).group_by(
        db.func.date(Transaction.timestamp), Transaction.transaction_type
    ).all()

    return [{"date": s.date, "total_amount": s.total_amount, "type": s.transaction_type} for s in summary]
