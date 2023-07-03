import sqlalchemy as db
from sqlalchemy import false, null, text, true, values
import psycopg2
import psycopg2.extras
from configparser import ConfigParser
import os

class dbBot():
    
    configFileName='.configSystem' 
    configFile=os.path.join(os.getcwd(), configFileName)
    sectionStr='DBServer'

    def __init__(self): 
        pass

    def readConfig(self, sectionStr, configFile):
        connectionStr={}
        try:
            # Read config file and setting   
            parser=ConfigParser()
            parser.read(configFile) 
            if parser is not None:
                if parser.has_section(sectionStr):
                    for item in parser.items(sectionStr):
                        connectionStr[item[0]]=item[1]
                    # print(connectionStr)
                    return connectionStr
                else:
                    print(f" No section {sectionStr} in config file ")
            else:
                print(f" No configuration file in the system!! ")
            
        except Exception as error:
            print(error)

    def connectToDB(self):
        cur=None
        conn=None
        connectionStr={}
        connectionStr=self.readConfig(self.sectionStr, self.configFile)
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

            
