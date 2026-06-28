import uuid
import os
import hmac
import hashlib
import base64
import requests


ESEWA_SECRET = os.getenv("ESEWA_SECRET_KEY")


def create_payment(amount):

    transaction_id = str(uuid.uuid4())

    return {

        "transaction_id": transaction_id,

        "amount": amount,

        "tax_amount": 0,

        "total_amount": amount,

        "product_code": "EPAYTEST",

        "product_service_charge": 0,

        "product_delivery_charge": 0,

        "signed_field_names": "total_amount,transaction_uuid,product_code",

        "signature": generate_signature(
            transaction_id,
            amount
        ),

        "success_url": "http://localhost:8000/payment/success",

        "failure_url": "http://localhost:8000/payment/failure"

    }


def generate_signature(transaction_id, amount):

    message = f"total_amount={amount},transaction_uuid={transaction_id},product_code=EPAYTEST"

    signature = hmac.new(
        ESEWA_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()

    return base64.b64encode(signature).decode()


def verify_payment(transaction_id, amount):

    url = (

        "https://rc-epay.esewa.com.np/api/epay/transaction/status/"

    )

    params = {

        "product_code": "EPAYTEST",

        "total_amount": amount,

        "transaction_uuid": transaction_id

    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    if data.get("status") == "COMPLETE":

        return True

    return False