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
            machine_name = args["client"]["hostname"]
            username = args["user"]
            os = args["client"]["system"]
            login_time = str2datetime(args["login_time"])
            logout_time = str2datetime(args["logout_time"])
            client_now = str2datetime(args["now"])
        except Exception as e:
	    raise e
            #raise Realog.Error(123, 'Invalid datetimestring: ' + e.message)

        #correction times
        time_diff = server_now - client_now
        logout_time += time_diff
        login_time += time_diff

        ret = {}
        try:
            print "INSERT INTO Comp_usage(CompID, User, LoginTime, LogoutTime) VALUES(%s, %s, %s, %s); UPDATE Computers SET OS=%s WHERE CompID LIKE %s" % (machine_name, username, login_time, logout_time, os, machine_name)
            c = self.db.getCursor()
            c.execute("""INSERT INTO Comp_usage(CompID, User, LoginTime, LogoutTime)
                        VALUES(%s, %s, %s, %s);
                        UPDATE Computers SET OS=%s WHERE CompID LIKE %s""", (machine_name, username, login_time, logout_time, os, machine_name))
        except Exception as e:
            raise Realog.Error(124, 'DB query failed: ' + e.message + e.__str__())

        ret['status'] = 0
        return ret

    def doPostProcessing(self):
        pass
    
