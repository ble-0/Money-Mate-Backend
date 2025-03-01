
import re

def parse_mpesa_sms(sms_content):

    amount_match = re.search(r"received KSh (\d+)", sms_content)
    if amount_match:
        amount = float(amount_match.group(1))
        transaction_type = "deposit"  or "transfered"
        return amount,  transaction_type
    return None, None
