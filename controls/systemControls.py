from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas import schemaLogin
from models import modelSystem
import tokenUtils 
import utilities

def get_token(form_data:OAuth2PasswordRequestForm , db:Session):
    user=db.query(modelSystem.User).filter(modelSystem.User.usercode == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials!! ") 
    if not utilities.verify_passwordHash(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password!! ")
    # Generate JWT Token
    token=tokenUtils.create_access_token({"sub":form_data.username})
    return {'access_token': token, 'token_type': 'bearer'} 
