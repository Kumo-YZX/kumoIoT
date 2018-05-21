import gwconf
import pymysql

def getTime():
    import datetime, gwconf
    localTime =datetime.datetime.now() +datetime.timedelta(hours =gwconf.zoneDelta)
    return localTime.strftime('%Y-%m-%d-%H-%M-%S')

class gwdb(object):

    def __init__(self):
        self.dbconn =pymysql.connect(host ='localhost',
                                     port =gwconf.dbport,
                                     user =gwconf.dbuser,
                                     password =gwconf.dbpasswd,
                                     db ='gwrdb',
                                     charset ='utf8mb4',
                                     cursorclass = pymysql.cursors.DictCursor
                                     )
    
    def executeSql(self, sqlCode, description ='execute'):
        with self.dbconn.cursor() as cursor:
            cursor.execute(sqlCode)
        self.dbconn.commit()
        print description +':done'
        return 1
    
    def querySql(self, sqlCode, description='query'):
        with self.dbconn.cursor() as cursor:
            cursor.execute(sqlCode)
            result =cursor.fetchall()
        print description +':done'
        return result

    def createTable(self, tableName):
        if tableName =='node':
            sqlCode ='CREATE TABLE node(' +\
                     'nodeid SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'nodename MEDIUMINT UNSIGNED NOT NULL,' +\
                     'token CHAR(16) NOT NULL,' +\
                     'PRIMARY KEY (nodeid));'
        elif tableName =='nvalue':
            sqlCode ='CREATE TABLE nvalue(' +\
                     'valueid INT UNSIGNED NOT NULL AUTO_INCREMENT,' +\
                     'ipaddress VARCHAR(15),' +\
                     'value FLOAT(16,8) NOT NULL,' +\
                     'time TIMESTAMP NOT NULL,' +\
                     'device SMALLINT UNSIGNED NOT NULL,' +\
                     'FOREIGN KEY (device) REFERENCES node(nodeid),' +\
                     'PRIMARY KEY (valueid));'
        else:
            return 'what do you want to do?'

        res =self.executeSql(sqlCode, 'createTable:'+tableName)
        return res

    def deleteTable(self, tableName):
        sqlCode ='DROP TABLE ' +tableName

        res =self.executeSql(sqlCode, 'dropTable:'+tableName)
        return res

    def closeConnection(self):
        res =self.dbconn.close()
        return res

class nodeTable(gwdb):

    def __init__(self):
        gwdb.__init__(self)
        self._tableName ='node'
        print 'node table init done!'

    def deleteNode(self, nodename =0):
        if nodename:
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE nodename=' +nodename +'\';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName +'\';'
        res =self.executeSql(sqlCode, 'deleteNode:'+str(nodename))
        return res

    def addNode(self, nodename, token):
        sqlCode ='INSERT INTO ' +self._tableName +' (nodename, token) VALUES (\'' +\
                 str(nodename) +'\', \'' +token +'\');'
        res =self.executeSql(sqlCode, 'addUser:'+nodename)
        return res
    
    def queryNode(self, nodename =0):
        if nodename:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE nodename=\'' +str(nodename) +'\';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +'\';'
        res =self.querySql(sqlCode, 'query:node:')
        return res

class valueTable(gwdb):

    def __init__(self):
        gwdb.__init__(self)
        self._tableName ='nvalue'
        print 'nvalue table init done!'

    def deleteValue(self, nodename =0):
        nodeqCode ='SELECT * FROM node WHERE nodename=\'' +str(nodename) +'\';'
        nodeInfo =self.querySql(nodeqCode, 'query:node:')
        if nodename:
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE device=' +nodeInfo[0]['nodeid'] +'\';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName +'\';'
        res =self.executeSql(sqlCode, 'deleteNode:'+str(nodename))
        return res
    
    def addValue(self, nodename, ip, value):
        nodeqCode ='SELECT * FROM node WHERE nodename=\'' +str(nodename) +'\';'
        nodeInfo =self.querySql(nodeqCode, 'query:node:')
        sqlCode ='INSERT INTO ' +self._tableName +' (ipaddress, value, device, time) VALUES (\'' +\
                 ip +'\', \'' +str(value) +'\', \'' +str(nodeInfo[0]['nodeid']) +'\', \''+getTime()  +'\');'
        res =self.executeSql(sqlCode, 'addnValue:'+str(nodename))
        return res

    def queryValue(self, nodename =0):
        if nodename:
            nodeqCode ='SELECT * FROM node WHERE nodename=\'' +str(nodename) +'\';'
            nodeInfo =self.querySql(nodeqCode, 'query:node:')
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE device=\'' +str(nodeInfo[0]['nodeid']) +'\';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +'\';'
        res =self.querySql(sqlCode, 'query:nValue'+str(nodename))
        return res

def testdb():
    import sys
    if sys.argv[1] =='cd':
        mydb =gwdb()
        # mydb.createTable('node')
        mydb.createTable('nvalue')
    elif sys.argv[1] =='an':
        mydb =nodeTable()
        mydb.addNode('1001', '72b4fa6ee1357f12')
        mydb.addNode('1002', 'd9795adf2ebb36d3')
        mydb.addNode('1003', 'fe3f024009412635')
        mydb.addNode('1004', '44ad0e0e85d05160')
    elif sys.argv[1] =='aq':
        mydb =nodeTable()
        print mydb.queryNode('1001')
        print mydb.queryNode('1002')
        print mydb.queryNode('1003')
        print mydb.queryNode('1004')
    elif sys.argv[1] =='av':
        mydb =valueTable()
        mydb.addValue(1001, '192.168.1.211', 36.0)
        mydb.addValue(1002, '192.168.1.212', 34.1)
        mydb.addValue(1003, '192.168.1.213', 36.4)
    elif sys.argv[1] =='qv':
        mydb =valueTable()
        print mydb.queryValue(1001)
        print mydb.queryValue(1003)
    else:
        pass

if __name__ =="__main__":
    testdb()