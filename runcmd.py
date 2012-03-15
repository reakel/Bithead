#!/usr/bin/env python

"""
Script for running commands on multiple computers
"""

from config import config
from database import Database
from sys import argv
import re
import os
from os import system

#Initialize db
Database.loadConfig(config)
db = Database()
c = db.getCursor()
#Regex for matching computer host names
re_comp_hn = re.compile('^k\d{4}$')

path = argv.pop(0)
nodes = set()
commands = []
rooms = set()
while argv:
    a = argv.pop(0)
    if a == 'do': break
    if re_comp_hn.match(a):
	nodes.add(a)
    elif a == 'all':
	rooms.clear()
	rooms.add('all')
	break
    else:
	rooms.add('\'' + a.upper() + '\'')

if rooms:
    querystr = "SELECT CompID FROM Computers WHERE OS = 'Linux'"
    r = rooms.pop()
    if r != 'all':
	rooms.add(r)
	querystr += " AND RoomID IN (" + ', '.join(rooms) + ')'
    c.execute(querystr)
    res = c.fetchone()
    while res:
	nodes.add(res[0])
	res = c.fetchone()

while argv:
    a = argv.pop(0)
    commands.append(a)

print "Running %i commands on %i nodes" % (len(commands), len(nodes))
print nodes

for node in nodes:
    pre = "ssh root@%s -o StrictHostKeyChecking=no" % node
    print "Running commands on", node
    for cmd in commands:
	system("%s '%s'" % (pre, cmd))
