
import re

def parse_mpesa_message(content):
    pattern = r"Amount: (\d+(\.\d{1,2})?)\s*Date: (\d{2}/\d{2}/\d{4})\s*Type: (\w+)"
    match = re.search(pattern, content)

    if match:
        amount = float(match.group(1))
        date = match.group(3)
        transaction_type = match.group(4)
        return amount, date, transaction_type
    return None, None, None
