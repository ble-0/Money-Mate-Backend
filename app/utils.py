import re

def parse_mpesa_message(message):
    # Example MPesa message format: "Confirmed. Ksh500 sent to John Doe..."
    match = re.search(r"Ksh(\d+\.?\d*)", message)
    if match:
        amount = float(match.group(1))
        return {"amount": amount, "category": "Unknown", "type": "expense"}
    return None
