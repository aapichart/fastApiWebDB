from configparser import ConfigParser
import configparser
import hashlib
import os

#######################################################################################################
# main config file management
#######################################################################################################

configFileName='.configSystem' 
configFile=os.path.join(os.getcwd(), configFileName)
# config Web server Parameters
webSectionStr='WebServer'
dbSectionStr='DBServer'
envStr='Authentication'

def mainCmd(createConfig):
    if os.path.exists(configFile):
        print(f" Config File already exist!! ")
    else: 
        # No config file in this zone
        config=configparser.ConfigParser()
        config[dbSectionStr]={
                'host':'localhost',
                'port':'5432',
                'dbname':'testDB',
                'user':'admin',
                'password':'testdb'}
        config[webSectionStr]={
                'host':'0.0.0.0',
                'port':'8000',
                'reload':'True'}
        config[envStr]={
                'saltkey':'Kowefoijwpkjdjk141we13240989823',
                'secretkey':'09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7',
                'algorithm':'HS256',
                'access_token_expire_minutes':'30',
                }

        with open(configFile, 'w') as defaultConfigFile:
           config.write(defaultConfigFile)
           print(f" Create new default config file!!! ")

def readConfigDBServer():
    dbServerConfig=getConfigVar(dbSectionStr)
    return dbServerConfig

def readAuthentication():
    envConfig=getConfigVar(envStr)
    return envConfig

def readConfigWebServer():
    webConfig=getConfigVar(webSectionStr)
    return webConfig

def getConfigVar(sectionVar):
    configStrList={} 
    try:
        # Read config file and setting   
        parser=ConfigParser()
        if os.path.exists(configFile):
            parser.read(configFile) 
            if parser is not None:
                if parser.has_section(sectionVar):
                    for item in parser.items(sectionVar):
                        configStrList[item[0]]=item[1] 
                    return configStrList
                else:
                    print(f" {sectionVar} not in Config file!! ")
            else:
                print(f" {configFileName} not Found!! ")
        else:
            print(f" {configFileName} not Found!! ")
    except configparser.Error as error:
        print(error)

#######################################################################################################
# This is the old password hashed algorithm using by php code
#######################################################################################################

def encryptPassword(inPassword):
    saltKeySection={}
    saltKeySection=readAuthentication()
    if len(saltKeySection)!=0:
        saltkey=saltKeySection['saltkey']
        inPassword=saltkey+inPassword    
        inPassword=inPassword.encode('utf-8')
        hashedPassword=hashlib.sha1(inPassword).hexdigest()
        return hashedPassword
    else:
        print(f" No saltkey for hasing process!! ")
#######################################################################################################

#######################################################################################################
# This is the old password hashed algorithm using by php code
#######################################################################################################

def verify_passwordHash(plainPassword, hashedPassword):
    hashedPlainPassword=encryptPassword(plainPassword)
    if hashedPlainPassword==hashedPassword:
        return True 
    else:
        print(f" Password is incorrect!! ")
        return False

#######################################################################################################
