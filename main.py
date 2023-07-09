import io
from typing import Annotated
import qrcode
from sqlalchemy import Boolean
from sqlalchemy.orm import Session
import uvicorn

from PIL import Image
from controls import systemControls
from imageProcedure import getImage 
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from starlette.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles 

from dbConnect import dbBot, sqlalchemyBot
from models import modelSystem
from models.modelSystem import User 
from routes.accRoute import routerAcc
from routes.invRoute import routerInven
from routes.finRoute import routerFin
from routes.hrMgtRoute import routerHr
from routes.purRoute import routerPur
from routes.systemRoute import routerSystem 

import utilities
from controls import systemControls
from dbConnect import get_db
from oauth2 import get_current_active_user, get_current_user 
from schemas.schemaLogin import Token

app = FastAPI()

@app.get('/',tags=['Welcome'])
async def root(current_user: Annotated[str, Depends(get_current_user)]):
    return {'FastAPI server': 'I''m AlphaBOT Server.',
            'current_user': current_user}

@app.post("/reqtoken", tags=['Welcome'])
async def reqtoken(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)):
  return systemControls.get_token(form_data, db)
                          
@app.get('/reqqr/{message}',tags=['Welcome'])
def genqr(message: str):
    img = qrcode.make(message)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg")

@app.get("/reqpass/{message}",tags=['Welcome'])
def generate(message: str):
    qr = qrcode.QRCode(box_size=2)
    qr.add_data(message)
    qr.make()
    img = qr.make_image()

    #  The second parameter => 1. pass, 2. wait, 3. anything = not allowed
    img1 = getImage(message, '')  

    img1.paste(img, (500,250))
    buf = io.BytesIO()
    img1.save(buf, format='JPEG')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg")

@app.get("/getpic/{message}",tags=['Welcome'])
def getpic(message: str):
    qr = qrcode.QRCode(box_size=2)
    qr.add_data(message)
    qr.make()
    img = qr.make_image()
    img1 = getImage(message, 'waiting')
    img1.paste(img, (500,250))
    return img1

@app.get("/getquery",tags=['Welcome'])
async def getquery():
    result=bot.exeQuery("select * from test order by num","")
    # result=bot.exeQuery("""
                        # INSERT INTO test (num, username, surname) 
                        # VALUES (%s,%s,%s);
                        # """,
                        # ('008','Test8','Test8Surname',))
    # result=bot.exeQuery("""
                        # UPDATE test set username=%s
                        # WHERE (num=%s)
                        # """,
                        # ('Testxxx','002'))
    # result=bot.exeQuery("""
                        # DELETE FROM test
                        # WHERE (num=%s)
                        # """,
                        # ('7',))
    html_content=f"""
    <html>
        <head>
           <title> Query DB Server </title> 
        </head>
        <body>
             {result} 
        </body>
    </html>
    """
    # return HTMLResponse(content=html_content, status_code=200)
    return JSONResponse(content=result)



# add more routes for each modules
app.include_router(routerAcc)
app.include_router(routerInven)
app.include_router(routerFin)
app.include_router(routerHr)
app.include_router(routerPur)
app.include_router(routerSystem)

# mouting path static for all images, css, and other resources
app.mount("/static", StaticFiles(directory="static"), name="static")

# create bot for connecting to psycopg2
bot=dbBot()

# crate meta schema for database model for using with sqlalchemy Bot
alBot=sqlalchemyBot()
alBot.openDBSession()
# Generate all table schemas for using, if it is not exist
if alBot.localEngine is not None:
    modelSystem.Base.metadata.create_all(alBot.localEngine)

# config Web server Parameters
webConfig=[]

if __name__ == "__main__":
    import argparse

    parse=argparse.ArgumentParser(description=" Create Interface for Control DBServer ")
    parse.add_argument('--createConfig', metavar=utilities.configFileName, required=False, help='Generate default config file')
    args=parse.parse_args()
    utilities.mainCmd(createConfig=args.createConfig)
    
    webConfig=utilities.readConfigWebServer()
    print(f" Config File loaded!! ")
    uvicorn.run("main:app", host=webConfig['host'], port=int(webConfig['port']), reload=Boolean(webConfig['reload']))

