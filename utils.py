from time import time

from base64 import urlsafe_b64encode

from pytoniq_core import begin_cell


def create_transaction(destination_address, amount, comment=None):
    if not comment:
        comment = f'Transaction of {amount} TON to {destination_address}'
    return {
        "valid_until": int(time() + 3600),
        "messages": [
            {
                "address": destination_address,
                "amount": str(amount*10 ** 9),
                "payload": urlsafe_b64encode(
                    begin_cell()
                    .store_uint(0, 32)  # op code for comment message
                    .store_string(comment)  # store comment
                    .end_cell()  # end cell
                    .to_boc()  # convert it to boc
                ).decode(),  # encode it to urlsafe base64
            }
        ],
    }
