import pymysql.cursors

class iotDB(object):

    def __init__(self, host ='localhost', user ='root', password ='passwd', db ='wxappDB'):
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
        pass
    
class userSet(iotDB):

    def __init__(self):
        iotDB.__init__(self)
        self._tableName ='users'
        print 'userSet init done'
    
    def deleteUser(self, userName ='NONE'):
        pass
