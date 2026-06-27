import uuid


def create_payment():

    transaction_id = str(uuid.uuid4())

    return {
        "transaction_id": transaction_id,
        "amount": 199
    }