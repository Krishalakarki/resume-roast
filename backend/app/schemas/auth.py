# request & response data shapes -> schemas 
# ->What data should come into or leave my API?

from pydantic import BaseModel #validation , convert json into python object
class UserCreate(BaseModel):
    email : str
    password : str

class UserLogin (BaseModel):
    email : str
    password : str