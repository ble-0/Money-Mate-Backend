def check_spending_limit(transactions, limit):
    total_spent = sum(t.amount for t in transactions if t.type == "expense")
    
    if total_spent > limit:
        return f"Warning! You've exceeded your spending limit of Ksh {limit}!"
    
    return "You're within your budget."
