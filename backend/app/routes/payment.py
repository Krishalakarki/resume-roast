from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.deps import get_current_user
from app.database.dependencies import get_db
from app.database.models import Payment

from app.services.esewa_service import create_payment, verify_payment


router = APIRouter()



# CREATE PAYMENT

@router.post("/create")
def create_esewa_payment(
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):


    payment = create_payment(199)



    new_payment = Payment(

        user_email=user,

        transaction_id=payment["transaction_id"],

        amount=199,

        status="PENDING"

    )



    db.add(new_payment)

    db.commit()



    return {


        "transaction_uuid": payment["transaction_id"],


        "amount": 199,


        "total_amount": 199,


        "product_code": "EPAYTEST",


        "product_service_charge": 0,


        "product_delivery_charge": 0,


        "signature": payment["signature"],



        # IMPORTANT
        "success_url":
        "http://localhost:8000/payment/success",



        "failure_url":
        "http://localhost:8000/payment/failure",



        "payment_url":
        "https://rc-epay.esewa.com.np/api/epay/main/v2/form"

    }







# CALLBACK FROM ESEWA

@router.get("/success")
def payment_success(

    transaction_uuid: str,

    db: Session = Depends(get_db)

):


    payment = db.query(Payment).filter(

        Payment.transaction_id == transaction_uuid

    ).first()



    if not payment:

        return {

            "error": "Payment not found"

        }




    result = verify_payment(

        transaction_uuid,

        payment.amount

    )




    if result:


        payment.status = "SUCCESS"

        db.commit()



        return {

            "message":
            "Payment successful. Premium unlocked"

        }




    payment.status = "FAILED"

    db.commit()



    return {

        "message":
        "Payment failed"

    }







# FAILURE CALLBACK

@router.get("/failure")
def payment_failure():

    return {

        "message":
        "Payment cancelled"

    }







# CHECK PAYMENT STATUS

@router.get("/status")
def payment_status(

    user: str = Depends(get_current_user),

    db: Session = Depends(get_db)

):


    payment = db.query(Payment).filter(

        Payment.user_email == user

    ).order_by(

        Payment.id.desc()

    ).first()



    if not payment:


        return {

            "paid": False

        }




    return {


        "paid": payment.status == "SUCCESS",


        "status": payment.status

    }