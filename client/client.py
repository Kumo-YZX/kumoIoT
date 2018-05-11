import urllib2

def loadModule(name, path):
    import os, imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), path))

loadModule('crypter2', '../cryptoz/crypter2.py')
import crypter2
loadModule('config', '../config.py')
import config

def send():
    myStr ='device=example&token=example&value=10.00'
    encStr =crypter2.encode(myStr, 1)
    request =urllib2.Request(config.serverUrl, data=encStr)
    receive =urllib2.urlopen(request).read()
    print receive

if __name__ =="__main__":
    send()