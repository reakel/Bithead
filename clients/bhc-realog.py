from bitheadclient import sendRequest
from datetime import datetime
from urllib import urlopen, urlencode
from sys import argv, exit
from os import environ
from pickle import dump,load, loads
from platform import uname
import socket

##-------------------------------------------------------------##
##                              Realog v. 2.0                              ##
##-------------------------------------------------------------##
##
## Client side Cross platform Realog
##      This program is written so that the computer usage 
##      on the student computer labs at NTNU can be 
##      monitored. bhc-realog can be run with two 
##      arguments: login or logout. Depending on the 
##      argument,  the program will write and read from a 
##      logfile, and send log entries to bithead.
##
## Last change: 17.08.2011 
##
## Reakel NTNU / Joachim Kruger
##                                                                                  ##
#############################################

# Set the path for the logfile with respect to the OS
p = environ.get('WINDIR')
if p:
    logpath = p + '\\Temp\\realogfile'
else:
    logpath = '/tmp/realogfile'

n = len(argv)
session = None
if n == 1:
    #Linux only
    session = environ.get('PAM_TYPE')
    if not session: 
	#realog was not started by PAM, exit
	exit(1)
    if session == 'open_session':
	session = 'login'
    elif session == 'close_session':
	print "close"
	session = 'logout' 
    else:
	print session
	exit(1)
elif n == 2:
    print "windows"
    #Windows
    session = argv[1]
else:
    exit(1)

#### LOGIN ####
## Write login time
if session == 'login':
    entries = []
    try:
        
        try:
            fload = open(logpath, 'r') 
            entries = load(fload)
            fload.close()
        except Exception as e:
            print e.message
                


        entry = {}
        # Win env has USERNAME; Linux  PAM env has PAM_USER
        entry['user'] = environ.get('USERNAME') or environ.get('PAM_USER')
        entry['login_time'] = str(datetime.now())

        entries.append(entry)
        fsave = open(logpath, 'w')
        dump(entries, fsave) 
        fsave.close()
    except IOError as e:
        entry = {}
        entry['now'] = str(datetime.now())
        entry['errormsg'] = socket.gethostname() + ': Could not open logfile when trying to save login time'
        entry['error'] = e
        sendRequest('realog', **entry)
        # Send Error message, Quit program
    finally:
        exit()


#### LOGOUT ####
## Write logout time and send  the log entry to bithead
if session == 'logout':
    print "logout"
    entries = []
    unsent_entries = []
    
    try:
        fload = open(logpath, 'r')
        entries = load(fload)
        fload.close()
    except IOError:
        entry = {}
        entry['errormsg'] = []
        entry['errormsg'].append( socket.gethostname() + ': Unable to read file. The login time has not been recorded for this computer. '   + str(datetime.now()) )     
        try:
            entry['now'] = str(datetime.now())
            sendRequest('realog', **entry)
        except Exception:
            pass
        exit()
    
    if len(entries):
        entry = entries[-1]
    else:
        entry = {}
        entry['errormsg'] = []
        entry['errormsg'].append( socket.gethostname() + ': Loaded an empty list. The login time has not been recorded for this computer. ' + str(datetime.now()))
        try:
            entry['now'] = str(datetime.now())
            sendRequest('realog', **entry)
        except Exception:
            entries.append(entry)
            try:
                fsave = open(logpath, 'w')
                dump(entries, fsave)
                fsave.close()
            except IOError:
                pass
        exit()
            
    
    
    if entries[-1].has_key('logout_time'):
        entry = {}
        entry['errormsg'] = []
        entry['errormsg'].append( socket.gethostname() + 'No recorded login time for this entry. '  + str(datetime.now()) )
        entries.append(entry) 
    else:
        entry = entries[-1]
        entry['logout_time'] =  str(datetime.now())
    
    for e in entries:
        e['now'] = str(datetime.now())
        try:
            sendRequest('realog', **e)
        except Exception:
            if not e.has_key('errormsg'):
                e['errormsg'] = []
            e['errormsg'].append('This entry has been tried sent '  + str(datetime.now()) )
            unsent_entries.append(e)

    try:
        fsave = open(logpath, 'w')
        dump(unsent_entries, fsave)
        fsave.close()
    except Exception:
        pass
    exit()
