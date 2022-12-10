from passlib.context import CryptContext
from logging import Handler

pwd_cxt =CryptContext(schemes=["bcrypt"],deprecated="auto")

class Hash():
    def bycrypt(password:str):
        return pwd_cxt.hash(password)
    
    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)