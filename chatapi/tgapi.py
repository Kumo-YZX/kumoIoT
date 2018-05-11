import urllib2
import json

def loadModule(name, path):
    import os, imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), path))

loadModule('config', '../config.py')
import config

class message(object):

    def __init__(self):
        self._apiUrl =apiUrl ='https://api.telegram.org/bot' +config.tgtoken
        print 'init with URL: ' +apiUrl

    def getUpdates(self):
        updateUrl =self._apiUrl +'/getUpdates'
        reply =urllib2.urlopen(updateUrl).read()
        return reply
    
    def sendMsg(self, chatId, textMsg =''):
        sendUrl =self._apiUrl +'/sendMessage'
        header ={'Content-type':'application/x-www-form-urlencoded', 'charset':'UTF-8'}
        paraDict ='chat_id='+str(chatId)+'&'+'text='+textMsg
        request =urllib2.Request(sendUrl, headers=header)
        reply =urllib2.urlopen(request, data=paraDict).read()
        return reply

if __name__ =="__main__":
    import sys
    msgObj =message()
    if sys.argv[1] =='getupd':
        print msgObj.getUpdates()
    elif sys.argv[1] =='senmsg':
        import datetime
        print msgObj.sendMsg(chatId=config.chatId, textMsg=('send test '+datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')))
    else:
        print 'what do you want to do?'
   