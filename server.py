import tornado.ioloop
import tornado.web

class mainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("page/homepage.html", mytitle="Welcome to KumoIoT API", parameter=["function1","function2","function3"])

def startApp():
    return tornado.web.Application([
        (r"/", mainHandler)
    ])

def main():
    app =startApp()
    app.listen(8093)
    tornado.ioloop.IOLoop.current().start()

if __name__ =="__main__":
    main()