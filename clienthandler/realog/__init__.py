#!/usr/bin/env python
from clienthandler import ClientHandler
from datetime import *

def str2datetime(str):
    tt = [int(_) for _ in str.split(',')]
    if len(tt) != 6:
	raise ClientHandler.Error(123, 'Invalid datetimestring')
    return datetime(*tt)

class Realog(ClientHandler):
    def getResponse(self):
	server_now = datetime.now()
        super(Realog,self).getResponse()
	args = self.args

	machine_name = args["compid"]
	username = args["user"]
	try:
	    login_time = str2datetime(args["login_time"])
	    logout_time = str2datetime(args["logout_time"])
	    client_now = str2datetime(args["now"])
	except Exception as e:
	    raise Realog.Error(123, 'Invalid datetimestring: ' + e.message)

	time_diff = server_now - client_now

	logout_time += time_diff
	login_time += time_diff

	ret = {}
	try:
	    c = self.db.getCursor()
	    c.execute("""INSERT INTO Comp_usage(CompID, User, LoginTime, LogoutTime)
			VALUES(%s, %s, %s, %s);
			UPDATE Computers SET OS='ubuntu' WHERE CompID LIKE %s""", (machine_name, username, login_time, logout_time, machine_name))
	except Exception as e:
	    raise Realog.Error(124, 'DB query failed: ' + e.message + e.__str__())

	ret['status'] = 0
	return ret

    def doPostProcessing(self):
	pass
    
