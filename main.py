import io
import os
import configparser
import qrcode
import uvicorn

from PIL import Image
from imageProcedure import getImage 
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse 
from starlette.responses import StreamingResponse

from dbConnect import dbBot


app = FastAPI()
bot=dbBot()

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
    result=bot.exeQuery("select * from test","")
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
    return HTMLResponse(content=html_content, status_code=200)

def mainCmd(createConfig):
    configFile=bot.configFile
    sectionStr=bot.sectionStr
    if os.path.exists(configFile):
        print(f" Config File already exist!! \n Can not generate default config file...")
    else: 
        # No config file in this zone
        config=configparser.ConfigParser()
        config[sectionStr]={
                'host':'localhost',
                'port':'5432',
                'dbname':'testdb',
                'user':'admin',
                'password':'testdb'}
        with open(configFile, 'w') as defaultConfigFile:
           config.write(defaultConfigFile)

if __name__ == "__main__":
    import argparse
    
    parse=argparse.ArgumentParser(description=" Create Interface for Control DBServer ")
    parse.add_argument('--createConfig', metavar=bot.configFileName, required=True, help='Generate default config file')
    args=parse.parse_args()
    mainCmd(createConfig=args.createConfig)
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


