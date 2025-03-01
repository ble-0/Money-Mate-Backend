from flask import Blueprint, jsonify

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/test", methods=["GET"])
def test_transactions():
    return jsonify({"message": "Transactions route is working!"}), 200
