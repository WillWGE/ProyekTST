from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import token2  

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

#to receive and verify jwt token (verify token hasil login)
def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )

    return token2.verify_token(token,credentials_exception)

#get_current_user akan menerima jwt token dari sub dependency oauth2_scheme yang terhubung dengan login (login akan generate jwt token)