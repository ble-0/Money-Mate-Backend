import re

def parse_mpesa_message(message):
    pattern = r"confirmed. Ksh(\d+\.?\d*).*?(?:from|to) (\w+)"
    match = re.search(pattern, message, re.IGNORECASE)

    if match:
        amount = float(match.group(1))
        recipient = match.group(2)
        return {"amount": amount, "recipient": recipient}
    
    return None
