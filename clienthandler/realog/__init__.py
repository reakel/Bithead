#!/usr/bin/env python
from clienthandler import ClientHandler

class Realog(ClientHandler):
    def getRespone(self):
        super(realog,self).getResponse()
        db = self.db.getCursor()
	args = self.args

	machine_name = args["machine_name"]
	username = args["username"]
	logout_time = args["Tk"]
	log_length = args["dT"]
	time = args["Tnk"]
	# Need to define the server's time, TnS
	time_difference = Tnk - Tns

	logout_time += time_difference
	login_time = logout_time - log_length

	ret = {}
	ret['status'] = 0
	try:
	    query = self.db.query("""INSERT INTO Comp_usage(CompID, User, LoginTime, LogoutTime)
			VALUES(%s, %s, %s, %s)
			UPDATE Computers SET OS='ubuntu' WHERE CompID LIKE %s""" %(machine_name, username, login_time, logout_time, machine_name))
	except:
	    raise realog.error(404, 'DB query failed')
	    self.printlog('DB query failed')
	    ret['status'] = 1

	self.printlog(db.store_result())
	
	return ret

    def doPostProsessing(self):
	pass
	
