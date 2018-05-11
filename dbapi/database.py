def loadModule(name, path):
    import os, imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), path))

loadModule('config', '../config.py')
import config

import pymysql.cursors

class iotDB(object):

    def __init__(self, host ='localhost', port=config.dbport, user =config.dbuser, password =config.dbpasswd, db ='myiotDB'):
        self.dbConnection =pymysql.connect(host =host,
                                           port =port,
                                           user =user,
                                           password =password,
                                           db =db,
                                           charset ='utf8mb4',
                                           cursorclass = pymysql.cursors.DictCursor
                                           )
    
    def executeSql(self, sqlCode, description ='execute'):
        with self.dbConnection.cursor() as cursor:
            cursor.execute(sqlCode)
        self.dbConnection.commit()
        print description +':done'
        return 1
    
    def querySql(self, sqlCode, description='query'):
        with self.dbConnection.cursor() as cursor:
            cursor.execute(sqlCode)
            result =cursor.fetchall()
        print description +':done'
        return result
    
    def createTable(self, tableName):
        if tableName =='User':
            sqlCode ='CREATE TABLE User(' +\
                     'userID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'username VARCHAR(48) NOT NULL,' +\
                     'firstname VARCHAR(48),' +\
                     'lastname VARCHAR(48),' +\
                     'gender VARCHAR(16),' +\
                     'usertgID INT UNSIGNED NOT NULL,' +\
                     'PRIMARY KEY (userID));'
        elif tableName =='dataDevice':
            sqlCode ='CREATE TABLE dataDevice(' +\
                     'dataDeviceID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'name VARCHAR(32) NOT NULL,' +\
                     'description MEDIUMTEXT,' +\
                     'location MEDIUMTEXT,' +\
                     'user SMALLINT UNSIGNED NOT NULL,' +\
                     'token CHAR(16) NOT NULL,' +\
                     'FOREIGN KEY (user) REFERENCES User(userID),' +\
                     'PRIMARY KEY (dataDeviceID));'
        elif tableName =='switchDevice':
            sqlCode ='CREATE TABLE switchDevice(' +\
                     'switchDeviceID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'name VARCHAR(32) NOT NULL,' +\
                     'description MEDIUMTEXT,' +\
                     'location MEDIUMTEXT,' +\
                     'user SMALLINT UNSIGNED NOT NULL,' +\
                     'status SMALLINT UNSIGNED NOT NULL,' +\
                     'token CHAR(16) NOT NULL,' +\
                     'FOREIGN KEY (user) REFERENCES User(userID),' +\
                     'PRIMARY KEY (switchDeviceID));'
        elif tableName =='dataValue':
            sqlCode ='CREATE TABLE dataValue(' +\
                     'dataValueID MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'time TIMESTAMP NOT NULL,' +\
                     'value FLOAT(16,8) NOT NULL,' +\
                     'device SMALLINT UNSIGNED NOT NULL,' +\
                     'FOREIGN KEY (device) REFERENCES dataDevice(dataDeviceID),' +\
                     'PRIMARY KEY (dataValueID));'
        elif tableName =='Msg':
            sqlCode ='CREATE TABLE Msg(' +\
                     'msgID MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'usertg INT UNSIGNED NOT NULL,' +\
                     'user SMALLINT UNSIGNED NOT NULL,' +\
                     'target ENUM(\'S\', \'R\'),' +\
                     'msgText MEDIUMTEXT,' +\
                     'time TIMESTAMP NOT NULL,' +\
                     'FOREIGN KEY (user) REFERENCES User(userID),' +\
                     'PRIMARY KEY (msgID));'
        elif tableName =='KeyTable':
            sqlCode ='CREATE TABLE KeyTable(' +\
                     'keyID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'keyStr CHAR(16) NOT NULL,' +\
                     'PRIMARY KEY (keyID));'
        else:
            return 'what do you want to do?'
        
        res =self.executeSql(sqlCode, 'createTable:'+tableName)
        return res

    def deleteTable(self, tableName):
        sqlCode ='DROP TABLE ' +tableName

        res =self.executeSql(sqlCode, 'dropTable:'+tableName)
        return res

    def closeConnection(self):
        res =self.dbConnection.close()
        return res
    
class userSet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='User'
        print 'User Set init done'
    
    def deleteUser(self, userName ='NONE'):
        if userName =='NONE':
            sqlCode ='DELETE FROM ' +self._tableName
        else:
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE username=' +userName
        res =self.executeSql(sqlCode, 'deleteUser:'+userName)
        return res
    
    def addUser(self, username, usertgID, firstname='NONE', lastname='NONE', gender='UNKNOWN'):
        sqlCode ='INSERT INTO ' +self._tableName +' (username, firstname, lastname, usertgID, gender) VALUES (\'' +\
                 username +'\', \'' +firstname +'\', \'' +lastname +'\', \'' +str(usertgID) +'\', \'' +gender +'\');'
        res =self.executeSql(sqlCode, 'addUser:'+username)
        return res

    def queryUser(self, userName='ALLU'):
        if userName =='ALLU':
            sqlCode ='SELECT * FROM ' +self._tableName
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE username=\'' +userName +'\';'
        res =self.querySql(sqlCode, 'query:User')
        return res

    def queryUserByID(self, userID):
        if userID:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE userID=\'' +str(userID) +'\';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName
        res =self.querySql(sqlCode, 'query:User')
        return res

class dataDeviceSet(iotDB):
    
    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='dataDevice'
        print 'dataDevice Set init done'

    def deleteDevice(self, deviceName='ALLD'):
        if deviceName =='ALLD':
            sqlCode ='DELETE FROM ' +self._tableName
        else:
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE name=' +deviceName
        res =self.executeSql(sqlCode, 'deleteDevice:'+deviceName)
        return res

    def addDevice(self, deviceName, user,token, description='NONE', location='NONE'):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, description, location, user, token) VALUES (\'' +\
                 deviceName +'\', \'' +description +'\', \'' +location +'\', \'' +str(user) +'\', \'' +token +'\');'
        res =self.executeSql(sqlCode, 'addDataDevice:'+deviceName)
        return res
    
    def queryDevice(self, deviceName='ALLD'):
        if deviceName =='ALLD':
            sqlCode ='SELECT * FROM ' +self._tableName
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE name=\'' +deviceName +'\';'
        res =self.querySql(sqlCode, 'query:dataDevice:')
        return res

class switchDeviceSet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='switchDevice'
        print 'switchDevice Set init done'

    def deleteDevice(self, deviceName='ALLS'):
        if deviceName =='ALLS':
            sqlCode ='DELETE FROM ' +self._tableName
        else:
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE name=' +deviceName
        res =self.executeSql(sqlCode, 'deleteDevice:'+deviceName)
        return res
    
    def addDevice(self, deviceName, user,token, description='NONE', location='NONE', status=0):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, description, location, user, token, status) VALUES (\'' +\
                 deviceName +'\', \'' +description +'\', \'' +location +'\', \'' +str(user) +'\', \'' +token+'\', \'' +str(status) +'\');'
        res =self.executeSql(sqlCode, 'addSwitchDevice:'+deviceName)
        return res

    def queryDevice(self, deviceName='ALLS'):
        if deviceName =='ALLS':
            sqlCode ='SELECT * FROM ' +self._tableName
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE name=\'' +deviceName +'\';'
        res =self.querySql(sqlCode, 'query:switchDevice:')
        return res
    
class dataValueSet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='dataValue'
        print 'switchDevice Set init done'

    def deleteValue(self, dataValueID=-1):
        if dataValueID ==-1:
            sqlCode ='DELETE FROM ' +self._tableName
        else:
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE dataValueID=' +str(dataValueID)
        res =self.executeSql(sqlCode, 'deletedataValue:'+str(dataValueID))
        return res

    def addDataValue(self, device, value=0):
        import datetime
        nowTime =datetime.datetime.now()+datetime.timedelta(hours=config.timeDelta)
        sqlCode ='INSERT INTO ' +self._tableName +' (time, value, device) VALUES (\'' +\
                 nowTime.strftime('%Y-%m-%d-%H-%M-%S') +'\', \'' +str(value) +'\', \'' +str(device) +'\');'
        res =self.executeSql(sqlCode, 'addDataValue:'+str(value))
        return res
    
    def queryData(self, device):
        sqlCode ='SELECT * FROM ' +self._tableName +' WHERE device=\'' +device +'\';'
        res =self.querySql(sqlCode, 'query:DataValue:'+str(device))
        return res

class msgSet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='Msg'
        print 'Msg Set init done'

    def deleteMsg(self, msgID=0):
        if msgID:
            sqlCode ='DELETE FROM ' +self._tableName +' HWERE msgID=' +str(msgID)
        else:
            sqlCode ='DELETE FROM ' +self._tableName
        res =self.executeSql(sqlCode, 'deleteMsg:'+str(msgID))
        return res

    def addMsg(self, userID, usertgID, target='S', msgText='NONE'):
        import datetime
        nowTime =datetime.datetime.now()+datetime.timedelta(hours=config.timeDelta)
        sqlCode ='INSERT INTO ' +self._tableName +' (time, usertg, user, target, msgText) VALUES (\'' +\
                 nowTime.strftime('%Y-%m-%d-%H-%M-%S') +'\',\'' +str(usertgID) +'\',\'' +str(userID) +'\',\'' +target +'\',\'' +msgText +'\');'
        res =self.executeSql(sqlCode, 'addMessage:'+msgText)
        return res
    
    def querymsg(self, userID):
        sqlCode ='SELECT * FROM ' +self._tableName +' WHERE userID=\'' +str(userID) +'\';'
        res =self.querySql(sqlCode, 'query:Message:'+str(userID))
        return res

class keySet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='KeyTable'
        print 'key Set init done'

    def deleteKey(self, keyID=0):
        if keyID:
            sqlCode ='DELETE FROM ' +self._tableName +' HWERE keyID=' +str(keyID)
        else:
            sqlCode ='DELETE FROM ' +self._tableName
        res =self.executeSql(sqlCode, 'deleteKey:'+str(keyID))
        return res

    def addKey(self, keyStr):
        if len(keyStr)!=16:
            print 'wrong key length!'
            return 0
        else:
            sqlCode ='INSERT INTO ' +self._tableName +' (keyStr) VALUES (\'' +keyStr +'\');'
        res =self.executeSql(sqlCode, 'addKeyStr:' +keyStr)
        return res
    
    def verfiyKey(self, keyID):
        sqlCode ='SELECT keyStr FROM ' +self._tableName +' WHERE keyID=\'' +str(keyID) +'\';'
        res =self.querySql(sqlCode, 'query:DataValue:'+str(keyID))
        return res

if __name__ =="__main__":
    pass