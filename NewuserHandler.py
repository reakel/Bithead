from ClientHandler import ClientHandler

class NewuserHandler(ClientHandler):
    logName = "Newuser"
    def __init__(self,socket,addr,args):
	super(NewuserHandler,self).__init__(socket,addr)
#	compID;user;loginTime;logoutTime;sysTime
	(self.compId,
	 self.loginTime,
	 self.logoutTime,
	 self.sysTime) = args
	if not (type(self.compId) is str 
		and type(self.loginTime) is int
		and type(self.logoutTime) is int
		and type(self.sysTime) is int):
	    raise Exception("Type error")

    def run(self):
	try:
	    self.socket.send("Hello World\n")
	    self.printLog("Sendt hello world")
	    self.printLog(str(self.readCommand()))
	finally:
	    self.socket.close()
	    


