import tornado.ioloop
import tornado.web
import tornado.template
import jinja2
import threading

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

class mainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("homepage.html", mytitle="Welcome to KumoIoT API", parameter=["function1","function2","function3"])

def startApp():
    return tornado.web.Application(template_loader=Jinja2Loader(),
     handlers=[
        (r"/", mainHandler)
    ])

def main():
    app =startApp()
    app.listen(8093)
    tornado.ioloop.IOLoop.current().start()

if __name__ =="__main__":
    main()