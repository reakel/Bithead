#!/usr/bin/env python
import bitheadclient as bhc
from sys import argv
import re

def printUsageAndExit():
    print "Usage:
    ./bhc-newuser.py <username>
    "
    exit(1)

class User(object):
    def __init__(self,username):
	self.username=username

    def dirExists(self):
	return False
    def 

if len(argv) > 1:
    un = argv[1]
    if re.search("[^A-Za-z0-9_-]",un):
	printUsageAndExit()
    



else:
    printUsageAndExit()


