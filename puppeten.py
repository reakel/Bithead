#!/usr/bin/env python
from config import config
from database import Database
from sys import argv
import yaml

dqfn = argv[1]
(host_name, sep, domain_name) = dqfn.partition(".")

Database.loadConfig(config)
db = Database()
c = db.getCursor()

res = c.execute("""SELECT Room.RoomID, PrinterURI FROM Computers LEFT JOIN Room ON Computers.RoomID = Room.RoomID WHERE CompID = %s""", ( host_name, ))
if not res: exit(1)
(room_id, printer_uri) = c.fetchone()
c.close()
db.close()

classes = {
    }
parameters = {
    }

if printer_uri and printer_uri.lower() != 'null':
    classes['defaultprinter'] = {
		'name': room_id,
		'uri': printer_uri,
	    }

node_config = {
    'classes': classes,
    'parameters': parameters,
    'environment': 'production',
    }

print yaml.dump(node_config)

