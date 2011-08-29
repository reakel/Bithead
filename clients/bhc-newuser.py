#!/usr/bin/env python
import bitheadclient as bhc
from sys import argv
import re
from os import path, stat, chmod, chown
from os import environ
from os.path import exists, isdir
from pwd import getpwnam



"""
This script checks if a user's directory exists with correct permissions.
If not it tries to fix it, contacting the server if necessary.
exi|ts with code != 0 if it cant be fixed
takes user name as argument
"""
pamtype = environ.get('PAM_TYPE')
if not pamtype or pamtype != 'open_session':
    exit(0)

homedir = '/home/WIN-NTNU-NO/'

un = environ('PAM_USER')
if re.search("[^A-Za-z0-9_-]",un): #check if argument is a valid user name
    exit(1)
s = getpwnam(un) #throws exception if un does not match a user 
userdir = s.pw_dir
uid = s.pw_uid
gid = s.pw_gid
if path.exists(userdir): #path to userdir exists
    if path.isdir(userdir): #userdir is a directory
	st = stat(userdir) 
	if uid == st.st_uid: 
	    if gid != st.st_gid:
		chown(userdir, -1, gid)
	    mode = oct(st.st_mode)[2:]
	    if mode != oct(0700):
		chmod(userdir,0700)		
	    exit(0)
    else:
	#homedir exists but is not dir
	exit(2)
try:
    res = bhc.sendRequest('newuser',user=un)
except Exception as e:
    print e.message
    exit(3)

else:
    printUsageAndExit()
