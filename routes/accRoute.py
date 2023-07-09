from click.types import BoolParamType
from fastapi import APIRouter,Request,Depends,status 
from fastapi.responses import HTMLResponse 
from sqlalchemy.orm import Session
from sqlalchemy import text

from controls import accControls 
from dbConnect import get_db
from schemas import schemaUsers 
from models.modelSystem import User 

routerAcc=APIRouter(
    tags=["accModule"]
)

@routerAcc.get("/accModule/test", response_class=HTMLResponse)
async def test(request:Request):
    return accControls.queryTest(request) 

@routerAcc.get("/accModule/getuser/{id}", status_code=status.HTTP_202_ACCEPTED)
async def getuser(id:int, db:Session = Depends(get_db)):
    return accControls.getuser(id, db)

@routerAcc.get("/accModule/getalluser/", status_code=status.HTTP_202_ACCEPTED)
async def getalluser(db:Session = Depends(get_db)):
    return accControls.getAllUser(db)

@routerAcc.post("/accModule/createuser", status_code=status.HTTP_201_CREATED)
async def createuser(request:schemaUsers.User, db:Session = Depends(get_db)):
    return accControls.createuser(request, db)

@routerAcc.put("/accModule/edituser/{id}", status_code=status.HTTP_202_ACCEPTED)
async def edituser(id, request:schemaUsers.User, db:Session = Depends(get_db)):
    return accControls.edituser(id, request, db)

@routerAcc.delete("/accModule/deleteuser/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteuser(id:int, db:Session = Depends(get_db)):
    return accControls.deleteuser(id, db)
