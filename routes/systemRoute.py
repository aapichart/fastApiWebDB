from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from controls import systemControls

from schemas import schemaLogin 
from dbConnect import get_db

routerSystem=APIRouter(
    tags=["systemModule"],
    prefix="/systemMoudle"
) 

# @routerSystem.post("/login",status_code=status.HTTP_202_ACCEPTED)
# async def login(request: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    # return systemControls.login(request, db)
