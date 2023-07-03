from click.types import BoolParamType
from fastapi import APIRouter,Request 
from fastapi.responses import HTMLResponse
from controls import accControls 
from dbConnect import dbBot

router=APIRouter(
    tags=["accModule"]
)

bot=dbBot()

@router.get("/accModule/test", response_class=HTMLResponse )
async def test(request:Request):
    return accControls.queryTest(request) 



