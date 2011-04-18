from Logable import Logable
from threading import Thread

class ClientHandler(Logable, Thread):
    addr = ''
    port = 0
    pre = ''
    buffer = ''
    cmds = []
    def __init__(self,socket,addr):
	super(ClientHandler,self).__init__()
	self.socket = socket
	self.socket.settimeout(5)
	self.addr, self.port = addr
	self.pre = '<' + str(self.addr) + '> '
	self.start()

    def printLog(self,str):
	super(ClientHandler,self).printLog(self.pre + str)

    def readCommand(self):
	while not self.cmds:
	    arr = self.buffer.split('$')
	    if len(arr) > 1:
		self.buffer = arr.pop()
		self.cmds = arr
		break
	    read =  self.socket.recv(8);
	    if not read: return ''
	    self.buffer += read.replace('\n','').replace('\r','')
	return self.cmds.pop(0).split(';')

	    



