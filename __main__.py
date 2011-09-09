#!/usr/bin/env python


import string, cgi, time
from os import curdir, sep
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ConfigParser import ConfigParser
import json
import re
from urlparse import parse_qs,unquote

from clienthandler import ClientHandler
from database import Database

configFiles = ['/etc/bithead.conf',sys.argv[0]+'/bithead.conf']
config = ConfigParser()
config.read(configFiles)

port = config.getint('http','port')
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
            handler = handlerClasses[cmd](self.client_address[0],args,db)
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

if __name__=='__main__':
    try:
        server = HTTPServer(('',port), MyRequestHandler)
        print "Started HTTPServer, listening to port %s" % (port)
        server.serve_forever()
    except KeyboardInterrupt:
        print 'TERM signal recieved, shutting down server'
        server.socket.close()
