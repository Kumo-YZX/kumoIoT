def loadModule(name, path):
    import os, imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), path))


from Crypto.Cipher import AES
from Crypto import Random

def encode(msg, keyIndex):
    loadModule('config', '../config.py')
    import config
    # format msg in lenth 224
    if len(msg) <232:
        msg +=(232-len(msg))*'&'
    elif len(msg) ==232:
        pass
    else:
        msg =msg[0:232]

    iv =Random.new().read(AES.block_size)
    cipher =AES.new(config.aesKey[keyIndex], AES.MODE_CFB, iv)
    strIndex =(8-len(str(keyIndex)))*'0' +str(keyIndex)
    encodeMsg =strIndex +iv +cipher.encrypt(msg)

    # print encodeMsg in hex
    outputStr =''
    for every in encodeMsg:
        outputStr +=((str(hex(ord(every)))[2:]).upper() +' : ')
    print outputStr

    return encodeMsg

if __name__ =="__main__":
    msg =encode('example string', 1)