exit() #remove this line

class HandlerTemplate(ClientHandler):
    def __init__(self): #Constructor
	super(HandlerTemplate,self).__init__() #always call constructor for superclass
	#declare member variables here if needed

    def getResponse(self): 
	#handles client request and returns a client response as a dict 
	#for time consuming processes use doPostProcessing()
	super(ClientHandler,self).getResponse() #this will print the request arguments to the log
	#self.args (dict): arguments from client
	#self.addr (string): client address
	#self.db (Database): database object
	#   use c = self.db.getCursor() to get a cursor (google MySQLdb)
	#self.printLog(str): print messages to log

	#handle client request here
	ret = {} #this is the response returned to client (dict)
	#ret['status'] defined and !=0 is interpreted by the client as a request failure 
	#best practice: raise ClientHandler.Error(errno, errmsg) (Exeption) on request failure


	return ret

    def doPostProcessing(self):
	pass
	#continue request handling after sending response
	#do not return anything
    
    @staticmethod
    def loadConfig(config):
	#load settings from default config file (/etc/bithead.conf)
	#Loaded settings should usualy be assigned to static variables
	#example, get a password from the 'templatehandler' section:
	#   HandlerTemplate.pass = config.get('templatehandler','pass')
	pass


