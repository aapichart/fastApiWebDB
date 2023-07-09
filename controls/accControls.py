from typing_extensions import deprecated
from fastapi import Request, HTTPException, status, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session 
from passlib.context import CryptContext
import os

from sqlalchemy.util import warn_limited

from dbConnect import dbBot 
from schemas import schemaUsers 
from models.modelSystem import User 
import utilities

def queryTest(request:Request):
    bot=dbBot()
    # load templates for rendering report
    templatesPath=os.path.join(os.getcwd(),'templates')
    templates=Jinja2Templates(directory=templatesPath)
    result=bot.exeQuery("select * from test order by num","")
    if result is not None:
        return templates.TemplateResponse(
                "report.html",
                {"request":request,"heading":result['header'],"data":result['data']}
                )
        # return {"username":templatesPath}
    else:
        # There is no record out of execution 
        return {"result":"Null"}

def getuser(id:int, db:Session):
    result=db.query(User).filter(User.id == id)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" User id {id} not found!! ")
    return result.first() 

def getAllUser(db:Session):
    result=db.query(User).all()
    return result 


def createuser(request:schemaUsers.User, db:Session):
    hashedPassword=utilities.encryptPassword(request.password)
    user1=User(usercode=request.code, username=request.name, password=hashedPassword, creatat=request.creatat, logonat=request.logonat)
    # user1=User(request)
    db.add(user1)
    db.commit()
    db.refresh(user1)
    return user1 

def edituser(id, request:schemaUsers.User, db:Session):
    result=db.query(User).filter(User.id == id)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" User id {id} not found!! ")
    else:
        # result.update( request, synchronize_session=False)
        hashedPassword=utilities.encryptPassword(request.password)
        result.update({User.usercode: request.code, User.username: request.name, User.password: hashedPassword}, synchronize_session=False)
    db.commit()
    return result.first()
    # return {"result":"update is done"}

def deleteuser(id:int, db:Session):
    result=db.query(User).filter(User.id == id)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f" User id {id} not found!! ")
    else:
        result.delete(synchronize_session=False)
    db.commit()
    return {"result":"delete is done"}

