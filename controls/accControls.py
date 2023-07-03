from fastapi import APIRouter,Request 
from fastapi.templating import Jinja2Templates
import os

from dbConnect import dbBot


def queryTest(request:Request):
    bot=dbBot()
    # load templates for rendering report
    templatesPath=os.path.join(os.getcwd(),'templates')
    templates=Jinja2Templates(directory=templatesPath)
    result=bot.exeQuery("select * from test order by num","")
    return templates.TemplateResponse(
            "report.html",
            {"request":request,"heading":result['header'],"data":result['data']}
            )
    # return {"username":templatesPath}


