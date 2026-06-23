from fastapi import APIRouter, Depends

from app.utils.deps import get_current_user

router = APIRouter()


@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):

    return {
        "message": "You are authorized ",
        "user": current_user
    }