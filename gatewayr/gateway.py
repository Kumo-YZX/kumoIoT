import tornado.ioloop
import tornado.web
import tornado.template
import datetime
import gwdb

def getTime():
    import datetime, gwconf
    localTime =datetime.datetime.now() +datetime.timedelta(hours =gwconf.zoneDelta)
    return localTime.strftime('%Y-%m-%d-%H-%M-%S')

class uploadData(tornado.web.RequestHandler):
    def get(self):
        nodeIP =self.request.remote_ip
        dataStr =self.request.query
        print 'connection from : ' +nodeIP +' data : ' +dataStr
        paraDict ={}
        for everyData in dataStr.split('&'):
            oneData =everyData.split('=')
            paraDict[oneData[0]] =oneData[1]
        nodedb =gwdb.nodeTable()
        nodeInfo =nodedb.queryNode(paraDict['name'])
        state =0
        if len(nodeInfo):
            if paraDict['token'] ==nodeInfo[0]['token']:
                valdb =gwdb.valueTable()
                valdb.addValue(paraDict['name'], nodeIP, paraDict['value'])
                state =1
            else:
                print 'wrong token'
        else:
            print 'node not exist'
        self.write({'status':state,'httpstatus':200,'nodeip':nodeIP,'time':getTime()})
    
    def post(self):
        nodeIP =self.request.remote_ip
        dataStr =self.request.body
        print 'connection from : ' +nodeIP +' data : ' +dataStr
        self.write({'status':True,'httpstatus':200,'nodeip':nodeIP,'time':getTime()})

class homePage(tornado.web.RequestHandler):
    def get(self):
        nodeIP =self.request.remote_ip
        dataStr =self.request.query
        print 'connection from : ' +nodeIP +' data : ' +dataStr
        self.write({'httpstatus':200,'data':'welcome to kumoIoT gatewayR','nodeip':nodeIP,'time':getTime()})

    def post(self):
        nodeIP =self.request.remote_ip
        dataStr =self.request.body
        print 'connection from : ' +nodeIP +' data : ' +dataStr
        self.write({'httpstatus':200,'data':'welcome to kumoIoT gatewayR','nodeip':nodeIP,'time':getTime()})

def gwapp():
    return tornado.web.Application(
        handlers=[
            (r"/", homePage)
            ,(r"/data/upload", uploadData)
            # ,(r"/data/cache", cacheData)
        ]
    )

def main():
    app =gwapp()
    app.listen(8095)
    tornado.ioloop.IOLoop.current().start()

if __name__ =="__main__":
    main()