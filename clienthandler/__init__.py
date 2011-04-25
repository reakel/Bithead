from logable import Logable
from threading import Thread

class ClientHandler(Logable):
    addr = ''
    port = 0
    pre = ''
    cmds = []
    def __init__(self,addr):
	self.addr = addr
	self.pre = '<' + str(self.addr) + '> '

    def printLog(self,str):
	super(ClientHandler,self).printLog(self.pre + str)
