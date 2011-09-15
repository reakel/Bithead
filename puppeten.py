#!/usr/bin/env python
from Bithead.config import config
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
printer_name = room_id
c.close()
db.close()
classes = []
parameters = {
    "room_id":room_id,
    }

if printer_name and printer_name.lower() != 'null':
#    classes.append("printer_%s" % room_id.lower())
    parameters["printer_name"] = room_id.lower() #printer_name has the same value as room_id for now

node_config = {
    'classes': classes,
    'parameters': parameters,
    'environment': 'production',
    }

print yaml.dump(node_config, default_flow_style=False).__str__().replace("{}","")
