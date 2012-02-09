#!/usr/bin/env python
"""
Script used by puppet for extracting relevant information about
a computer from the Bithead DB
"""
from config import config
from database import Database
from sys import argv
import yaml

dqfn = argv[1]
(host_name, sep, domain_name) = dqfn.partition(".")

Database.loadConfig(config)
db = Database()
c = db.getCursor()

#Get information from the db
res = c.execute("""SELECT Room.RoomID, PrinterURI FROM Computers LEFT JOIN Room ON Computers.RoomID = Room.RoomID WHERE CompID = %s""", ( host_name, ))
if not res: exit(1) #Computer was not found, exit
(room_id, printer_uri) = c.fetchone()
printer_name = room_id
c.close()
db.close()


"""
Build the data structure that is to be passed to puppet.
"""

classes = []		    #List of puppet classes that should be included

parameters = {		    #Dict with names and values for puppet parameters. 
    "room_id":room_id,	    #Referred to in Puppet by $param_name
    }

environment = 'production'  #Environment for the computer

if printer_name and printer_name.lower() != 'null':
    parameters["printer_name"] = room_id.lower() #printer_name has the same value as room_id for now

node_config = {
    'classes': classes, 
    'parameters': parameters,
    'environment': environment,
    }

#Serialize structure as yaml formatted string
#Removal of '{}' is necessary for campatibility with Puppet.
print yaml.dump(node_config, default_flow_style=False).__str__().replace("{}","") 
