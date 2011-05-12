#!/usr/bin/env python


import string, cgi, time
from os import curdir, sep
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ConfigParser import ConfigParser
import json
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
	db = Database()
	try:
	    path = self.path
	    cmd,args = path.partition('?')[0::2]
	    cmd = cmd.lower().lstrip('/')
	    if cmd not in handlerClasses.keys():
		raise HTTPException()
	    args = self.parseArgs(args)
	    handler = handlerClasses[cmd](self.client_address[0],args,db)
	    handler.printLog('Connected')
	    response = handler.getResponse()
	    if not 'status' in response.keys(): 
		response['status'] = '0'
	    self.send_default_response()
	    self.wfile.write(json.dumps(response))
	    handler.doPostProcessing()
	except HTTPException:
	    self.send_error(404,'DIE')
	except ClientHandler.Error as (errno, errstr):
	    self.send_default_response()
	    self.wfile.write(json.dumps({'status':errno}))
	except Exception:
	    self.send_error(404,'DIE')
	finally:
	    db.close()
    
    def send_default_response(self):
	self.send_response(200)
	self.send_header('Cache-Control', 'no-cache, must-revalidate')
	self.send_header('Content-type', 'text/html')
	self.end_headers()

    def do_POST(self):
	self.send_error(404, 'DIE')
    
    def parseArgs(self, args):
	if not args: return {}
	args = args.split('&')
	ret = {}
	for arg in args:
	    arg = arg.strip(' ')
	    arg = arg.split('=')
	    n = len(arg)
	    if n == 1:
		key = arg[0]
		value = True
	    elif len(arg) == 2:
		key, value = arg
	    else:
		raise HTTPException()
	    
	    ret[key] = value
	return ret

if __name__=='__main__':
    try:
	server = HTTPServer(('',port), MyRequestHandler)
	print "Started HTTPServer, listening to port %s" % (port)
	server.serve_forever()
    except KeyboardInterrupt:
	print 'TERM signal recieved, shutting down server'
	server.socket.close()
