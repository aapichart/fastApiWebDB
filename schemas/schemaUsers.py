from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    code: str
    name: str
    password: str
    creatat: datetime 
    logonat: datetime  

    
