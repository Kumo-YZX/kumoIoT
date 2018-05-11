import database

def main():
    import sys
    con =sys.argv[1]
    if con =='create':
        mydb =database.iotDB()
        for tableName in ['User','dataDevice','switchDevice','dataValue','Msg']: #'User','dataDevice','switchDevice','dataValue','Msg','KeyTable'
            mydb.createTable(tableName)
    elif con =='adduser':
        infos =sys.argv[2].split('-')
        mydb =database.userSet()
        mydb.addUser(infos[0],infos[1],infos[2],infos[3],infos[4])
    elif con =='adddatad':
        infos =sys.argv[2].split('-')
        mydb =database.dataDeviceSet()
        mydb.addDevice(infos[0],infos[1],infos[2])
    elif con =='addswid':
        infos =sys.argv[2].split('-')
        mydb =database.switchDeviceSet()
        mydb.addDevice(infos[0],infos[1],infos[2])
    elif con =='adddatav':
        infos =sys.argv[2].split('-')
        mydb =database.dataValueSet()
        mydb.addDataValue(infos[0],infos[1])
    elif con =='addmsg':
        infos =sys.argv[2].split('-')
        mydb =database.msgSet()
        mydb.addMsg(infos[0],infos[1],infos[2],infos[3])
    elif con =='addkey':
        mydb =database.keySet()
        mydb.addKey(sys.argv[2])
    elif con =='schuser':
        mydb =database.userSet()
        if len(sys.argv) ==3:
            res =mydb.queryUser(sys.argv[2])
        else:
            res =mydb.queryUser()
        for every in res:
            print every
    elif con =='schdatad':
        mydb =database.dataDeviceSet()
        if len(sys.argv) ==3:
            res =mydb.queryDevice(sys.argv[3])
        else:
            res =mydb.queryDevice()
        for every in res:
            print every
    elif con =='schswid':
        mydb =database.switchDeviceSet()
        if len(sys.argv) ==3:
            res =mydb.queryDevice(sys.argv[3])
        else:
            res =mydb.queryDevice()
        for every in res:
            print every
    elif con =='schdatav':
        mydb =database.dataValueSet()
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