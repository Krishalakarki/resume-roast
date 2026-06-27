from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class RoastHistory(Base):
    __tablename__ = "roast_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(255), index=True)

    filename = Column(String(255))
    resume_text = Column(Text)

    ai_response = Column(Text)


class Payment(Base):

    __tablename__ = "payments"


    id = Column(Integer, primary_key=True)

    user_email = Column(String(255))

    transaction_id = Column(String(255))

    amount = Column(Integer)

    status = Column(String(50))