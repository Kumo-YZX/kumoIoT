import pymysql.cursors
import config

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
                     'name CHAR(16) NOT NULL,' +\
                     'description MEDIUMTEXT,' +\
                     'gender TINYTEXT,' +\
                     'PRIMARY KEY (userID));'
        elif tableName =='dataDevice':
            sqlCode ='CREATE TABLE dataDevice(' +\
                     'dataDeviceID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'name CHAR(16) NOT NULL,' +\
                     'description MEDIUMTEXT,' +\
                     'location MEDIUMTEXT,' +\
                     'user SMALLINT UNSIGNED NOT NULL,' +\
                     'FOREIGN KEY (user) REFERENCES User(userID),' +\
                     'PRIMARY KEY (dataDeviceID));'
        elif tableName =='switchDevice':
            sqlCode ='CREATE TABLE switchDevice(' +\
                     'switchDeviceID SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'name CHAR(16) NOT NULL,' +\
                     'description MEDIUMTEXT,' +\
                     'location MEDIUMTEXT,' +\
                     'user SMALLINT UNSIGNED NOT NULL,' +\
                     'status SMALLINT UNSIGNED NOT NULL,' +\
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
        elif tableName =='keyTable':
            sqlCode ='CREATE TABLE keyTable(' +\
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
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE name=' +userName
        res =self.executeSql(sqlCode, 'deleteUser:'+userName)
        return res
    
    def addUser(self, userName, description='NONE', gender='UNKNOWN'):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, description, gender) VALUES (\'' +userName +'\', \'' +description +'\', \'' +gender +'\');'
        res =self.executeSql(sqlCode, 'addUser:'+userName)
        return res

    def queryUser(self, userName='ALLU'):
        if userName =='ALLU':
            sqlCode ='SELECT * FROM ' +self._tableName
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE name=\'' +userName +'\';'
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

    def addDevice(self, deviceName, user, description='NONE', location='NONE'):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, description, location, user) VALUES (\'' +\
                 deviceName +'\', \'' +description +'\', \'' +location +'\', \'' +str(user) +'\');'
        res =self.executeSql(sqlCode, 'addDataDevice:'+deviceName)
        return res
    
    def queryDevice(self, deviceName='ALLD'):
        if deviceName =='ALLD':
            sqlCode ='SELECT * FROM ' +self._tableName
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +'WHERE name=\'' +deviceName +'\';'
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
    
    def addDevice(self, deviceName, user, description='NONE', location='NONE', status=0):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, description, location, user, status) VALUES (\'' +\
                 deviceName +'\', \'' +description +'\', \'' +location +'\', \'' +str(user) +'\', \'' +str(status) +'\');'
        res =self.executeSql(sqlCode, 'addSwitchDevice:'+deviceName)
        return res

    def queryDevice(self, deviceName='ALLS'):
        if deviceName =='ALLS':
            sqlCode ='SELECT * FROM ' +self._tableName
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +'WHERE name=\'' +deviceName +'\';'
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
        nowTime =datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        sqlCode ='INSERT INTO ' +self._tableName +' (time, value, device) VALUES (\'' +\
                 nowTime +'\', \'' +str(value) +'\', \'' +str(device) +'\');'
        res =self.executeSql(sqlCode, 'addDataValue:'+str(value))
        return res
    
    def queryData(self, device):
        sqlCode ='SELECT * FROM ' +self._tableName +'WHERE device=\'' +device +'\';'
        res =self.querySql(sqlCode, 'query:DataValue:'+str(device))
        return res

class keySet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='keyTable'
        print 'key Set init done'

    def deleteKey(self, keyID=-1):
        if keyID<0:
            sqlCode ='DELETE FROM ' +self._tableName
        else:
            sqlCode ='DELETE FROM ' +self._tableName +' HWERE keyID=' +keyID
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
        sqlCode ='SELECT * FROM ' +self._tableName +'WHERE device=\'' +keyID +'\';'
        res =self.querySql(sqlCode, 'query:DataValue:'+str(keyID))
        return res

def main():
    import sys
    con =sys.argv[1]
    if con =='create':
        mydb =iotDB()
        for tableName in ['keyTable']:
            mydb.createTable(tableName)
    elif con =='adduser':
        infos =sys.argv[2].split('-')
        mydb =userSet()
        mydb.addUser(infos[0],infos[1],infos[2])
    elif con =='adddatad':
        infos =sys.argv[2].split('-')
        mydb =dataDeviceSet()
        mydb.addDevice(infos[0],infos[1])
    elif con =='addswid':
        infos =sys.argv[2].split('-')
        mydb =switchDeviceSet()
        mydb.addDevice(infos[0],infos[1])
    elif con =='adddatav':
        infos =sys.argv[2].split('-')
        mydb =dataValueSet()
        mydb.addDataValue(infos[0],infos[1])
    elif con =='addkey':
        mydb =keySet()
        mydb.addKey(sys.argv[2])
    elif con =='schuser':
        mydb =userSet()
        if len(sys.argv) ==3:
            res =mydb.queryUser(sys.argv[2])
        else:
            res =mydb.queryUser()
        for every in res:
            print every
    elif con =='schdatad':
        mydb =dataDeviceSet()
        if len(sys.argv) ==3:
            res =mydb.queryDevice(sys.argv[3])
        else:
            res =mydb.queryDevice()
        for every in res:
            print every
    elif con =='schswid':
        mydb =switchDeviceSet()
        if len(sys.argv) ==3:
            res =mydb.queryDevice(sys.argv[3])
        else:
            res =mydb.queryDevice()
        for every in res:
            print every
    elif con =='schdatav':
        mydb =dataValueSet()
        if len(sys.argv) ==3:
            res =mydb.queryData(sys.argv[3])
        else:
            res =mydb.queryData('1')
        for every in res:
            print every
    else:
        print 'what do you want to do?'

if __name__ =="__main__":
    main()