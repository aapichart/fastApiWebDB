import io
import os
import configparser
import qrcode
from sqlalchemy import Boolean
import uvicorn

from PIL import Image
from imageProcedure import getImage 
from fastapi import FastAPI, Response, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse 
from starlette.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles 

from dbConnect import dbBot
from routes.accRoute import router
from routes.invRoute import router2
from routes.finRoute import router3
from routes.hrMgtRoute import router4
from routes.purRoute import router5
from routes.systemRoute import router6

app = FastAPI()

@app.get('/')
async def root():
    return {'FastAPI server': 'I''m AlphaBOT Server.'}

@app.get('/reqqr/{message}')
def genqr(message: str):
    img = qrcode.make(message)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg")

@app.get("/reqpass/{message}")
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

@app.get("/getpic/{message}")
def getpic(message: str):
    qr = qrcode.QRCode(box_size=2)
    qr.add_data(message)
    qr.make()
    img = qr.make_image()
    img1 = getImage(message, 'waiting')
    img1.paste(img, (500,250))
    return img1

@app.get("/getquery")
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

app.include_router(router)
app.include_router(router2)
app.include_router(router3)
app.include_router(router4)
app.include_router(router5)
app.include_router(router6)

# mouting path static for all images, css, and other resources
app.mount("/static", StaticFiles(directory="static"), name="static")

bot=dbBot()
webSectionStr='WebServer'
configFile=bot.configFile
sectionStr=bot.sectionStr
webConfig=[]

def readConfigWebServer():
    try:
        if os.path.exists(configFile):
            config=configparser.ConfigParser()
            config.read(configFile)
            webConfig=config[webSectionStr]
            return webConfig
        else: 
            # No config file in this zone
            print(f" No Config File for Web Server!! ")
    except configparser.Error as error:
        print(error)

def mainCmd(createConfig):
    if os.path.exists(configFile):
        print(f" Config File already exist!! ")
    else: 
        # No config file in this zone
        config=configparser.ConfigParser()
        config[sectionStr]={
                'host':'localhost',
                'port':'5432',
                'dbname':'testDB',
                'user':'admin',
                'password':'testdb'}
        config[webSectionStr]={
                'host':'0.0.0.0',
                'port':'8000',
                'reload':'True'}

        with open(configFile, 'w') as defaultConfigFile:
           config.write(defaultConfigFile)

if __name__ == "__main__":
    import argparse

    parse=argparse.ArgumentParser(description=" Create Interface for Control DBServer ")
    parse.add_argument('--createConfig', metavar=bot.configFileName, required=False, help='Generate default config file')
    args=parse.parse_args()
    mainCmd(createConfig=args.createConfig)
    
    webConfig=readConfigWebServer()
    print(f" Config File loaded!! ")
    uvicorn.run("main:app", host=webConfig['host'], port=int(webConfig['port']), reload=Boolean(webConfig['reload']))

