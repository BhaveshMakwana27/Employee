from jose import jwt
import database,models
from schema import Token,TokenData
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta

SECRET_KEY = 'ksjdfhlsdf'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_TIMEOUT = 30

oauth2_scheme = OAuth2PasswordBearer('user/login')

def create_token(data:dict):
    to_encode=data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_TIMEOUT))
    to_encode.update({'exp':expire_time})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_access_token(token:str,CredentialsException):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str|None = payload.get('user_id')
        user_type:str|None = payload.get('user_type')
        if id is None:
            raise CredentialsException
        token_data = TokenData(id=id,user_type=user_type)
    except:
        raise CredentialsException
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    CredentialsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could Not validate credentials',
                                          headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,CredentialsException)

    return True
