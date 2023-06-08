from PIL import Image, ImageDraw

def getImage(message: str, imgtype: str):
    if imgtype == 'wait':
        img = Image.open('images/waiting.jpg')
    elif imgtype == 'pass':
        img = Image.open('images/passImg.jpg')
    else:
        img = Image.open('images/NotAllowed.jpg')
    dl = ImageDraw.Draw(img)
    dl.text((36, 36), message, fill=(255,255,255))
    return img 
