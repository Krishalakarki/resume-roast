from jose import jwt  #create , verify , decode tokens
from datetime import datetime, timedelta #curent time and expiry date
import os
from dotenv import load_dotenv
load_dotenv ()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #valid for 60 min
def create_access_token(data:dict):
    to_encode = data.copy() #copy original data so it wont be modified
    expire =datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#It takes a user’s data (like user ID or email) 
# and turns it into a secure digital login pass called a JWT token.





