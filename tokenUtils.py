from jose import JWSError, JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from schemas.schemaLogin import TokenData 
from models.modelSystem import User
import utilities

configAuthen=utilities.readAuthentication()
SECRET_KEY=configAuthen['secretkey']
ALGORITHM=configAuthen['algorithm']
ACCESS_TOKEN_EXPIRE_MINUTES=configAuthen['access_token_expire_minutes']


def create_access_token(data: dict):
    to_encode=data.copy() 
    expire=datetime.utcnow()+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    encode_jwt=jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def verify_token(token: str,db:Session, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username:str = payload.get("sub") 
        if username is None:
            raise credentials_exception
        token_data=TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user=db.query(User).filter(User.usercode==username).first()
    if user is None:
        raise credentials_exception
    return token_data

