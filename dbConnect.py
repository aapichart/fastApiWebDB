from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import false, null, text, true, values
import psycopg2
import psycopg2.extras
from configparser import ConfigParser
import os

import utilities

#######################################################################################################
# This bot is for sqlalchemy Package
class sqlalchemyBot():

    # define object in class for database calling
    connectionStrUrl=''
    localEngine=None
    localSession=None

    def __init__(self):
        pass
   
    def genDataBaseUrl(self):
        connectionStr={}
        connectionStrUrl=''
        try:
            connectionStr=utilities.readConfigDBServer()
            self.connectionStrUrl="postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(**connectionStr)
            print(connectionStrUrl)
        except Exception as error:
            print(error)

    def getConnectionStr(self):
        return self.connectionStrUrl;

    def openDBSession(self):
        # self.genDataBaseUrl(self.sectionStr, self.configFile)
        self.genDataBaseUrl()
        if self.connectionStrUrl is not None:
            try:
                self.localEngine=create_engine(self.connectionStrUrl)
                self.localSession=sessionmaker(bind=self.localEngine, autocommit=False, autoflush=False) 
                return self.localSession
            except SQLAlchemyError as error:
                print(error)

#######################################################################################################
# This function is used to calling object and bind engine to session for execute database as sqlalchemy
# sqlalchemy session.execute do not use SQL Language 
# if you want to use SQL, please use dbBot - or psycopg2 instead
#######################################################################################################
Base=declarative_base()
def get_db():
    alBot=sqlalchemyBot()
    localSession=alBot.openDBSession()
    if localSession is not None:
        db=localSession()
        try:
            yield db 
        finally:
            db.close()
#######################################################################################################


#######################################################################################################
# This bot is for psycopg2 Package
class dbBot():
    
    def __init__(self): 
        pass

    def readConfig(self):
        connectionStr={}
        try:
            connectionStr=utilities.readConfigDBServer()
            return connectionStr
        except Exception as error:
            print(error)

    def connectToDB(self):
        cur=None
        conn=None
        connectionStr={}
        # connectionStr=self.readConfig(self.sectionStr, self.configFile)
        connectionStr=self.readConfig()
        if connectionStr is not None:
            try:
                conn = psycopg2.connect(**connectionStr) 
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
                print(f" Connect to database server successfully!! ")
            except psycopg2.OperationalError as error:
                print(error)
        else:
            print(f" Config file has no database configuration!! ")
        return cur, conn

    def exeQuery(self, queryStr, parameterStr):
        cur=None
        conn=None
        returnList={}
        cur, conn=self.connectToDB()
        if conn is not None:
            try:
                if cur is not None:
                    cur.execute(queryStr, parameterStr)
                    # collect column name from result
                    columnName=[] 
                    columnName=[i[0] for i in cur.description] 
                    returnList['header']=columnName
                    outputList=[]
                    for record in cur:
                        outputList.append(record)
                    returnList['data']=outputList
                    cur.close()
                    return returnList
            except Exception as error:
                print(error)
            finally:
                conn.commit()
                conn.close()

            
