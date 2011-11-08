from logable import Logable

class ClientHandler(Logable):
    config = {}
    def __init__(self,addr,addr_str,args,db,**kwargs):
	super(ClientHandler,self).__init__(**kwargs)
        self.db = db
        self.addr = addr
	self.addr_str = addr_str
        self.args=args

    def printLog(self,str, *args, **kwargs):
	extra = { 'clientip': self.addr_str }
	if kwargs.get('extra'):
	    kwargs['extra'].update(extra)
	else:
	    kwargs['extra'] = extra
        super(ClientHandler,self).printLog(str, *args, **kwargs)

    def getResponse(self):
        #for debugging #self.printLog('arguments: ' + self.args.__str__())
        return self.args

#doPostProcessing() is called after getResponse()
    def doPostProcessing(self):
        pass
            


    @staticmethod
    def loadConfig(config):
        pass

    class Error(Exception):
        pass
