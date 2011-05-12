from logable import Logable

class ClientHandler(Logable):
    config = {}
    def __init__(self,addr,args,db):
	self.db = db
	self.addr = addr
	self.args=args
	self.pre = '<' + str(self.addr) + '> '

    def printLog(self,str):
	super(ClientHandler,self).printLog(self.pre + str)

    def getResponse(self):
	self.printLog('arguments: ' + self.args.__str__())
	return self.args


    @staticmethod
    def loadConfig(config):
	pass

    class Error(Exception):
	pass
