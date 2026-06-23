from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app.utils.jwt import create_access_token
from app.database.dependencies import get_db
from app.database.models import User

from app.schemas.auth import UserCreate, UserLogin

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------
# SIGNUP
# -------------------------
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"email": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }