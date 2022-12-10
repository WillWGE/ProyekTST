from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Float


class toko(Base):
    __tablename__="toko"

    id=Column(Integer,primary_key=True,index=True)
    nama=Column(String)
    lokasi=Column(String)
    tv_ad=Column(Float)
    instagram_ad=Column(Float)
    newspaper_ad=Column(Float)

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
     