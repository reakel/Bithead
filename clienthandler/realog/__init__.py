#!/usr/bin/env python
from clienthandler import ClientHandler

class Realog(ClientHandler):
    def getRespone(self):
        super(realog,self).getResponse()
        db = self.db.getCursor()
	args = self.args

	machine_name = args["machine_name"]
	username = args["username"]
	login_time = args["login_time"]
	logout_time = args["logout_time"]
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
	self.printlog(db.fetchone())
	
	return ret

    def doPostProsessing(self):
	pass
	
