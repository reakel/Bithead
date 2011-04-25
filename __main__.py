#!/usr/bin/env python

import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ConfigParser import ConfigParser
import json
from clienthandler import ClientHandler

from database import Database

handlers = [ 'realog',
	     'newuser',
	     'postinstall',
	     'pubkey']


configFiles = [u'/etc/bithead.conf']
config = ConfigParser()
config.read(configFiles)

port = config.getint('http','port')
Database.loadConfig(config)

handlerClasses = {}

for handler in handlers:
    c = handler.capitalize()
    print handler, c
    exec "from clienthandler.%s import %s" % (handler, c)
    handlerClasses[handler] = eval(c)
    handlerClasses[handler].loadConfig(config)


class HTTPException(Exception):
    pass

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
	try:
	    path = self.path
	    cmd,args = path.partition('?')[0::2]
	    cmd = cmd.lower().lstrip('/')
	    if cmd not in handlerClasses.keys():
		raise HTTPException()
	    args = self.parseArgs(args)
	    handler = handlerClasses[cmd](self.client_address[0],args)
	    handler.printLog('Connected')
	    response = handler.getResponse()
	    if not 'status' in response.keys(): 
		response['status'] = '0'
	    self.send_response(200)
	    self.send_header('Content-type', 'text/html')
	    self.end_headers()
	    self.wfile.write(json.dumps(response))
	    return
	except HTTPException:
	    self.send_error(404,'DIE')
	except ClientHandler.Error as (errno, errstr):
	    self.send_response(200)
	    self.send_header('Content-type', 'text/html')
	    self.end_headers()
	    self.wfile.write(json.dumps({'status':errno}))
	except Exception:
	    self.send_error(404,'DIE')

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








def main():
    
    try:
	server = HTTPServer(('',port), MyHandler)
	print "Started HTTPServer, listening to port %s" % (port)
	server.serve_forever()
    except KeyboardInterrupt:
	print 'TERM signal recieved, shutting down server'
	server.socket.close()

if __name__=='__main__':
    main()
