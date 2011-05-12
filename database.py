import MySQLdb
from ConfigParser import ConfigParser

class Database(object):
    host = None
    user = None
    passwd = None
    db = None
    conn = None

    @staticmethod
    def loadConfig(config):
	section = 'database'
	Database.host = config.get(section, 'host')
	Database.user = config.get(section, 'user')
	Database.passwd = config.get(section, 'passwd')
	Database.db = config.get(section, 'db')

    def __dbConnect(self):
	if not self.conn or not self.conn.open:
	    self.conn = MySQLdb.connect (host = self.host,
		    user = self.user,
		    passwd = self.passwd,
		    db = self.db)
    
    def getCursor(self):
	self.__dbConnect()
	return self.conn.cursor()

    def close(self):
	if self.conn and self.conn.open:
	    self.conn.close()

if __name__ == '__main__':
    configFiles = [u'/etc/bithead.conf']
    config = ConfigParser()
    config.read(configFiles)
    Database.loadConfig(config)
    db = Database()
    c = db.getCursor()
    c.execute("""SELECT * FROM Computers""")
    for row in c.fetchall():
	print row
    c.close()
    db.close()
