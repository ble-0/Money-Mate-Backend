from flask import Blueprint, request, jsonify
from app.services.analytics import get_total_income_expense, get_transaction_summary

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/summary", methods=["GET"])
def analytics_summary():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    summary = get_total_income_expense(user_id)
    return jsonify(summary), 200

@analytics_bp.route("/transactions", methods=["GET"])
def transactions_summary():
    user_id = request.args.get("user_id", type=int)
    period = request.args.get("period", "monthly")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    transactions = get_transaction_summary(user_id, period)
    return jsonify(transactions), 200
