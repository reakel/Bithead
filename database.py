import MySQLdb

class Database:
    def __init__(self,host, user, passwd, db):
	self.host=host
	self.user = user
	self.passwd = passwd
	self.db = db
	self.conn = False

    def dbConnect(self):
	if self.conn and not self.conn.open:
	    self.conn = MySQLdb.connect (host = self.host,
		    user = self.user,
		    passwd = self.passwd,
		    db = self.db)
    
    def getCursor(self):
	if not self.conn or not self.conn.open:
	    self.dbConnect()
	return self.conn.cursor()





