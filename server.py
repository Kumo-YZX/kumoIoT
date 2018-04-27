import tornado.ioloop
import tornado.web
import tornado.template
import jinja2
import threading
import crypter

class myTemplate(object):
    def __init__(self, template_instance):
        self.template_instance =template_instance

    def generate(self, **kwargs):
        return self.template_instance.render(**kwargs)

class Jinja2Loader(tornado.template.BaseLoader):
    def __init__(self, **kwargs):
        self.jinja_environment =jinja2.Environment(loader=jinja2.FileSystemLoader('pages/'), **kwargs)
        self.templates ={}
        self.lock =threading.RLock()

    def resolve_path(self, name, parent_path =None):
        return name

    def _create_template(self, name):
        template_instance =myTemplate(self.jinja_environment.get_template(name))
        return template_instance

class homePage(tornado.web.RequestHandler):
    def get(self):
        self.render("homepage.html", mytitle="Welcome to KumoIoT API", parameter=["function1","function2","function3"])

class uploadData(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        dataStr =self.request.query
        print 'connection from : ' +userIp +'data : ' +dataStr
        paraDict ={}
        for everyData in dataStr.split('&'):
            oneData =everyData.split('=')
            paraDict[oneData[0]] =oneData[1]
        viewList =['User : '+paraDict['user'],'Token : '+paraDict['token'],'Name : '+paraDict['name'],'Value : '+paraDict['value']]

        self.render('homepage.html', mytitle='You are using GET method : ' +userIp, parameter=viewList)
    
    def post(self):
        userIp =self.request.remote_ip
        encryptData =self.request.query
        print 'connection from : ' +userIp +'Data : ' +encryptData
        decryptData =crypter.decode(encryptData)
        paraDict ={}
        for everyData in decryptData.split('&'):
            oneData =everyData.split('=')
            paraDict[oneData[0]] =oneData[1]
        viewList =['User : '+paraDict['user'],'Token : '+paraDict['token'],'Value : '+paraDict['value']]

        self.render('homepage.html', mytitle='You are using encrypted POST method : ' +userIp, parameter=viewList)

class catchData(tornado.web.RequestHandler):
    def get(self):
        pass
        
    def post(self):
        pass

def startApp():
    return tornado.web.Application(template_loader=Jinja2Loader(),
    handlers=[
        (r"/", homePage),
        (r"/data/upload", uploadData),
        (r"/data/catch", catchData)
    ])

def main():
    app =startApp()
    app.listen(8093)
    tornado.ioloop.IOLoop.current().start()

if __name__ =="__main__":
    main()