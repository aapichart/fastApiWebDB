import sqlalchemy as db
from sqlalchemy import null, text, true, values
import psycopg2
import psycopg2.extras
from configparser import ConfigParser
import os

class dbBot():
   
    hostname = ''
    dbname = ''
    port = ''
    user = ''
    password = ''
    
    def __init__(self):
        # Read config file and setting   
        parser=ConfigParser()
        configPath=os.path.join(os.getcwd(),'.configSystem')
        parser.read(configPath) 
        # self.hostname= parser.get('DBServer','HOSTNAME')
        print(self.hostname)
        self.hostname="10.135.70.133"
        # self.dbname=dbServer['DBNAME']
        self.dbname="testDB"
        # self.port=dbServer.get('PORT_NO')
        self.port='5433'
        # self.user=dbServer.get('USERNAME')
        self.user="root"
        # self.password=dbServer.get('PASSWD')
        self.password="chartx.123"

    def connectToDB(self):
        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    ) as self.conn:
                self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        except Exception as error:
            print(error)

    def buildDict(self, outputList):
        columnName=[] 
        dataDict={}
        # collect column name from result
        columnName=[i[0] for i in self.cur.description] 
        # build jason output as dictionary list in python 
        recCount=1
        for record in self.cur.fetchall():
            for countInt in range(len(columnName)):
                dataDict[columnName[countInt]]=record[countInt]
            outputList[f"{recCount}"]=dataDict
            # clear after append for another record
            recCount+=1
            dataDict={}
        return outputList

    def exeQuery(self, queryStr, parameterStr):
        try:
            outputList={}
            self.connectToDB()
            self.cur.execute(queryStr, parameterStr)
            outputList=self.buildDict(outputList)
            return outputList
        except Exception as error:
            print(error)
        finally:
            self.cur.close()
            self.conn.commit()

            
