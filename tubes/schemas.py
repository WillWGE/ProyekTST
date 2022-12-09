from fastapi import FastAPI
from pydantic import BaseModel
from typing import List,Optional


#pydantic model
class toko(BaseModel):
    nama:str
    lokasi:str
    tv_ad:float
    instagram_ad:float
    newspaper_ad:float

class User(BaseModel):
    name:str
    email:str
    password:str
    
class showToko(BaseModel):
    nama:str
    lokasi:str
    tv_ad:float
    instagram_ad:float
    newspaper_ad:float
    class Config():
        orm_mode=True

class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode=True
  
class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] =None

class atribut(BaseModel):
    tv_ad:float
    instagram_ad:float
    newspaper_ad:float

class prediction(BaseModel):
    prediction:int

