import io
import qrcode

from PIL import Image
from imageProcedure import getImage 
from fastapi import FastAPI
from starlette.responses import StreamingResponse


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

