from fastapi import APIRouter, Depends

from app.utils.deps import get_current_user
from app.services.esewa_service import create_payment


router = APIRouter()


@router.post("/create")
def create_esewa_payment(
    user:str = Depends(get_current_user)
):

    payment = create_payment()


    return {

        "message":"Payment created",

        "user":user,

        "payment":payment
    }