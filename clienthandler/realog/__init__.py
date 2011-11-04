#!/usr/bin/env python
from clienthandler import ClientHandler
from datetime import *

def str2datetime(str):
    return datetime.strptime(str,'%Y-%m-%d %H:%M:%S.%f')

class Realog(ClientHandler):
    def getResponse(self):
        server_now = datetime.now()
        super(Realog,self).getResponse()
        args = self.args
        #args should contain:
        #compid, user, login_time, logout_time,os , now (time on the client used for time correction)

        try:
	    if (args.get('error')): return { 'error':args.get('error') }
            machine_name = args["client"]["hostname"]
            username = args["user"]
            os = args["client"]["system"]
	    if not args.get('login'):
		login_time = str2datetime(args["login_time"])
		logout_time = str2datetime(args["logout_time"])
		client_now = str2datetime(args["now"])
        except Exception as e:
	    raise e
            #raise Realog.Error(123, 'Invalid datetimestring: ' + e.message)

        #correction times
	if not args.get('login'):
	    time_diff = server_now - client_now
	    logout_time += time_diff
	    login_time += time_diff

        ret = {}
        try:
            c = self.db.getCursor()
	    if args.get('login'):
		c.execute("""UPDATE Computers SET LoggedIn = NOW() WHERE CompID = %s""", machine_name)
	    else:
		c.execute("""INSERT INTO Comp_usage(CompID, User, LoginTime, LogoutTime) 
			VALUES(%s, %s, %s, %s);""", (machine_name, username, login_time, logout_time))
		c.execute("""UPDATE Computers SET OS=%s WHERE CompID LIKE %s""", (os, machine_name))
		c.execute("""UPDATE Computers SET LoggedIn = 0 WHERE CompID = %s""", machine_name)
        except Exception as e:
            raise Realog.Error(124, 'DB query failed: ' + e.message + e.__str__())
	finally:
	    c.close()

        ret['status'] = 0
        return ret

    def doPostProcessing(self):
        pass
    
