from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 

from dbConnect import get_db
from models.modelSystem import User
import tokenUtils


oauth2_scheme= OAuth2PasswordBearer(tokenUrl="reqtoken")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:Session=Depends(get_db)):
    credentials_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    return tokenUtils.verify_token(token, db, credentials_exception)

def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


