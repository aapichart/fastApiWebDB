from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy.sql import func 

from dbConnect import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq', start=1), primary_key=True, index=True)
    usercode = Column(String)
    username = Column(String)
    password = Column(String)
    creatat = Column(DateTime(timezone=True), server_default=func.now())
    logonat = Column(DateTime(timezone=True), onupdate=func.now())
