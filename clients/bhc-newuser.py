#!/usr/bin/env python
import bitheadclient as bhc
from sys import argv
import re

def printUsageAndExit():
    print "Usage: ./bhc-newuser.py <username>"
    exit(1)


if len(argv) > 1:
    un = argv[1]
    if re.search("[^A-Za-z0-9_-]",un):
        printUsageAndExit()
    bhc.sendRequest('newuser',user=un)
else:
    printUsageAndExit()


