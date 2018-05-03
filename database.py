import pymysql.cursors

class iotDB(object):

    def __init__(self, host ='localhost', user ='root', password ='passwd', db ='myiotDB'):
        self.dbConnection =pymysql.connect(host =host,
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
        result ={}
        with self.dbConnection.cursor() as cursor:
            cursor.execute(sqlCode)
            result =cursor.fetchone()
        print description +':done'
        return 1, result
    
    def createTable(self, tableName):
        if tableName =='User':
            sqlCode ='CREATE TABLE User(' +\
                     'userID UNSIGNED SMALLINT NOT NULL AUTO_INCREMENT,' +\
                     'name CHAR(16) NOT NULL,' +\
                     'description MEDUIMTEXT,' +\
                     'gender TINYTEXT,' +\
                     'PRIMARYKEY (userID));'
        elif tableName =='dataDevice':
            sqlCode ='CREATE TABLE dataDevice(' +\
                     'dataDeviceID UNSIGNED SAMLLINT NOT NULL AUTO_INCREMENT,' +\
                     'name CHAR(16) NOT NULL,' +\
                     'description MEDUIMTEXT,' +\
                     'location MEDUIMTEXT,' +\
                     'user UNSIGNED SMALLKEY NOT NULL,' +\
                     'FOREIGNKEY (user) REFERENCES User(userID),' +\
                     'PRIMARYKEY (dataDeviceID));'
        elif tableName =='switchDevice':
            sqlCode ='CREATE TABLE switchDevice(' +\
                     'switchDeviceID UNSIGNED SAMLLINT NOT NULL AUTO_INCREMENT,' +\
                     'name CHAR(16) NOT NULL,' +\
                     'description MEDUIMTEXT,' +\
                     'location MEDUIMTEXT,' +\
                     'user UNSIGNED SMALLKEY NOT NULL,' +\
                     'status UNSIGNED SMALLINT NOT NULL' +\
                     'FOREIGNKEY (user) REFERENCES User(userID),' +\
                     'PRIMARYKEY (switchDeviceID));'
        elif tableName =='dataValue':
            sqlCode ='CREATE TABLE dataValue(' +\
                     'dataValueID UNSIGNED MEDIUMINT NOT NULL AUTO_INCREMENT,' +\
                     'time TIMESTAMP NOT NULL' +\
                     'value FLOAT(16,8) NUT NULL' +\
                     'device UNSIGNED SMALLINT NOT NULL' +\
                     'FOREIGNKEY (device) REFERENCES dataDevice(dataDeviceID)' +\
                     'PRIMARYKEY (dataValueID));'
        elif tableName =='key':
            sqlCode ='CREATE TABLE key(' +\
                     'keyID UNSIGNED TINYINT NOT NULL AUTO_INCREMENT,' +\
                     'keyStr CHAR(16) NOT NULL' +\
                     'PRIMARYKEY (keyID));'
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
        self._tableName ='users'
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

    def queryUser(self, userName='ALL'):
        sqlCode ='SELECT * FROM ' +self._tableName +' WHERE name=\'' +userName +'\';'
        state, res =self.querySql(sqlCode, 'query:User')
        if state:
            return res
        else:
            return 'NOT FOUND'

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
        state, res =self.querySql(sqlCode, 'query:dataDevice:')
        if state:
            return res
        else:
            return 'NOT FOUND'

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
        state, res =self.querySql(sqlCode, 'query:switchDevice:')
        if state:
            return res
        else:
            return 'NOT FOUND'
    
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
        nowTime =datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        sqlCode ='INSERT INTO ' +self._tableName +' (time, value, device) VALUES (\'' +\
                 nowTime +'\', \'' +str(value) +'\', \'' +str(device) +'\';'
        res =self.executeSql(sqlCode, 'addDataValue:'+str(value))
        return res
    
    def queryData(self, device):
        sqlCode ='SELECT * FROM ' +self._tableName +'WHERE device=\'' +device +'\';'
        state, res =self.querySql(sqlCode, 'query:DataValue:'+str(device))
        if state:
            return res
        else:
            return 'NOT FOUND'

class keySet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='key'
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
            sqlCode ='INSERT INTO ' +self._tableName +' (keyStr) VALUES (\'' +keyStr +'\';'
        res =self.executeSql(sqlCode, 'addKeyStr:' +keyStr)
        return res
    
    def verfiyKey(self, keyID):
        sqlCode ='SELECT * FROM ' +self._tableName +'WHERE device=\'' +keyID +'\';'
        state, res =self.querySql(sqlCode, 'query:DataValue:'+str(keyID))
        if state:
            return res
        else:
            return 'NOT FOUND'

def main():
    import sys
    import config
    con =sys.argv[1]
    if con =='create':
        mydb =iotDB(password=config.dbpasswd)
        for tableName in ['User','dataDevice','switchDevice','dataValue','key']:
            mydb.createTable(tableName)
    elif con =='adduser':
        infos =sys.argv[2].split('&')
        mydb =userSet()
        mydb.addUser(infos[0],infos[1],infos[2])
    elif con =='adddatad':
        infos =sys.argv[2].split('&')
        mydb =dataDeviceSet()
        mydb.addDevice(infos[0],infos[1])
    elif con =='addswid':
        infos =sys.argv[2].split('&')
        mydb =switchDeviceSet()
        mydb.addDevice(infos[0],infos[1])
    elif con =='adddatav':
        infos =sys.argv[2].split('&')
        mydb =dataValueSet()
        mydb.addDataValue(infos[0],infos[1])
    elif con =='addkey':
        mydb =keySet()
        mydb.addKey(sys.argv[0])

if __name__ =="__main__":
    main()