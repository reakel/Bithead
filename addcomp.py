#!/usr/bin/env python
from config import config
from database import Database
from sys import argv
import re

class Computer(object):
    def __init__(self,id,**kwargs):
	self.db = kwargs['db']
	self.k_nr = id.lower()
	self.room = kwargs['room']
	self.mac = kwargs['mac'].lower()
	self.is_updated = None
	self.validate()

    def validate(self):
	if not re.match(r"^\w+$", self.k_nr) :
	    raise Exception("Invalid k_nr or room_id")
	res = re.match(r"^[0-9a-f]{2}([^0-9a-f]?)([0-9a-f]{2}\1){4}[0-9a-f]{2}$", self.mac) #Validating mac using arbitrary separator
	if not res:
	    raise Exception("Invalid mac")
	sep = res.group(1)
	self.mac = self.mac.replace(sep,'')
	self.mac = int(self.mac,16) #convert mac to base-10 integer

    def is_created(self):
	c = self.db.getCursor()
	if c.execute("""SELECT (RoomID=%s AND Mac = %s) as updated FROM Computers WHERE CompID = %s""", (self.room.id, self.mac, self.k_nr)):
	    self.is_updated = c.fetchone()[0] > 0
	    return True
	return False

    def update(self):
	c = self.db.getCursor()
	if self.is_updated:
	    return True
	res = c.execute("""UPDATE Computers SET Mac = %s,RoomID = %s WHERE CompID = %s""", (self.mac, self.room.id, self.k_nr))
	return (res > 0)

    def create(self):
	c = self.db.getCursor()
	res = c.execute("""INSERT INTO Computers(CompID, RoomID, Mac) VALUES (%s, %s, %s)""", (self.k_nr, self.room.id, self.mac))
	return (res > 0)

    def create_or_update(self):
	if self.is_created():
	    return self.update()
	else:
	    return self.create()
	    
class Room(object):
    def __init__(self, room_id, db):
	self.id = room_id.lower()
	self.db = db
	self.validate()

    def validate(self):
	c = self.db.getCursor()
	if not re.match(r"^[\w-]+$", self.id):
	    raise Exception("Invalid room id")
	if not c.execute("""SELECT RoomID FROM Room WHERE RoomID = %s""", (self.id, )):
	    ans = None
	    while ans == None:
		print "Room %s does not exist, create? (y/n)" % self.id
		ans = raw_input().lower()
		if ans[0] == "y":
		    c.execute("""INSERT INTO Room(RoomID) VALUES (%s)""", (self.id,))
		if ans[0] == "n":
		    print "Could not add computer"
		    exit(1)
		else:
		    print "Please answer yes or no"
		    ans = None
	else:
	    print "Room %s exists" % self.id





if __name__=='__main__':
    if len(argv) != 4:
	print "Usage: addcomp roomid compid mac"
	exit(1)

    try:
	Database.loadConfig(config)
	db = Database()
	comp = Computer(argv[2],room=Room(argv[1],db), mac=argv[3], db=db) 
	if comp.create_or_update():
	    print "Successfully created or updated %s" % comp.k_nr
	else:
	    print "Could not create or update %s" % k_nr

    except Exception as e:
	print e
    finally:
	db.close()
