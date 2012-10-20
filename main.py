#!/usr/bin/env python


import string, cgi, time, socket
from os import curdir, sep, mkdir, chmod
from os.path import exists, isdir
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import json
import re
from urlparse import parse_qs,unquote
from config import config
from clienthandler import ClientHandler
from database import Database
from time import sleep
from logable import Logable
import logging

from securehttpserver import SecureHTTPServer


port = config.getint('server','port')
logdir = config.get('server','logdir')
logfile = "%s/server" % logdir
logfile_http = "%s/http" % logdir
errorlog = "%s/error" % logdir
LOG_FORMAT = "%(levelname)s -- %(asctime)19.19s [%(name)s] <%(clientip)s>: %(message)s"
LOG_LEVEL = logging.DEBUG

if exists(logdir):
    if not isdir(logdir):
	print "Log path %s exists, but is not a directory" % logdir
	exit(2)
else:
    try:
	mkdir(logdir)
	chmod(logdir,0700)
	print "Logdir created with path %s" % logdir
    except:
	print "Could not create logdir %s" % logdir
	exit(2)

HTTPLOGGER = logging.Logger(name="HTTP", level=LOG_LEVEL)
fh = logging.FileHandler(logfile_http)
fh.setFormatter(logging.Formatter(fmt="%(asctime)19.19s: %(message)s"))
HTTPLOGGER.addHandler(fh)
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, filename = logfile)
#sys.stdout = open(logfile_http,'a',1)
#sys.stderr = open(errorlog, 'a', 1)

Database.loadConfig(config)

handlerClasses = {}

i = 0
for item in config.items('handlers'):
    handler, active = item
    active = bool(int(active))
    if not active:
        print 'Skipped module:', handler
        continue
    c = handler.capitalize()
    print 'Loading module:', handler
    exec "from clienthandler.%s import %s" % (handler, c)
    handlerClasses[handler] = eval(c)
    handlerClasses[handler].loadConfig(config)
    i = i+1

print 'Successfully loaded %i modules' % (i)




class HTTPException(Exception):
    pass

class MyRequestHandler(BaseHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def log_message(self,format, *args):
	HTTPLOGGER.info(format, *args, extra={'clientip':'1236'})

    def do_GET(self):
	db = None
        try:
	    try:
		self.args
	    except AttributeError:
		self.args = {}
            path = self.path
            cmd,args = path.partition('?')[0::2]
            cmd = cmd.lower().lstrip('/')
            if cmd not in handlerClasses.keys():
                raise HTTPException()
            args = self.parseArgs(args)
            if self.args: args.update(self.args)
            #self.validateArgs(args)
            args=self.args
	    db = Database()
            handler = handlerClasses[cmd](self.client_address[0],self.address_string(),args,db)
            handler.printLog('Connected')
            response = handler.getResponse()
            if not 'status' in response.keys(): 
                response['status'] = '0'
            self.send_default_response()
            self.wfile.write(json.dumps(response))
            print "DONE"
            handler.doPostProcessing()
        except HTTPException:
            self.send_error(404,'DIE')
        except ClientHandler.Error as (errno, errstr):
            self.send_default_response()
            print 'Error:', errno, errstr
            self.wfile.write(json.dumps({'status':errno}))
        except Exception as e:
            type = e.__class__.__name__
            print "Exception"
            print type
            msg = json.dumps({ 'exeption': type, 'args':e.args})
            self.send_error(404,'Generic DIE: ' + msg)
        finally:
	    if db:
		db.close()
    
    def send_default_response(self):
        self.send_response(200)
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        try:
            posts = self.rfile.read(int(self.headers['Content-Length']))
            posts = unquote(posts)
	    print posts
            self.args = json.loads(posts)
            self.do_GET()
        except Exception as e:
            self.send_error(404,'Generic DIEEE: ' + e.message + ' ' + e.__class__.__name__)
            print e.message



    def validateArgs(self,args):
        argscheck = re.compile('[^ a-zA-Z0-9,;:_\\-+\.]')
        for item in args.items():
            key,value = item
            if argscheck.search(key) or argscheck.search(value):
                raise HTTPException()

    
    def parseArgs(self, args):
        if not args: return {}
        args = parse_qs(args, True, True) 
        for key in args.keys():
            value = args[key][0]
            args[key] = value
        return args

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class ThreadedSecureHTTPServer(ThreadingMixIn, SecureHTTPServer):
    pass

