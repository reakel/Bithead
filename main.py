#!/usr/bin/env python

import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ConfigParser import ConfigParser

from database import Database

handlers = [ 'realog',
	     'newuser',
	     'postinstall']

handlerClasses = {}

for handler in handlers:
    c = handler.capitalize()
    print handler, c
    exec "from handlers.%s import %s" % (handler, c)
    handlerClasses[handler] = eval(c)

handlerClasses['realog']('sdf').printLog('hello')

class HTTPException(Exception):
    pass

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
	try:
	    path = self.path
	    cmd,args = path.partition('?')[0::2]
	    cmd = cmd.lower().replace('/','')
	    args = args.split('&')
	    if cmd not in handlerClasses.keys():
		raise HTTPException()
	    handlerClasses[cmd](self.client_address[0]).printLog('connected')
	    self.send_response(200)
	    self.send_header('Content-type', 'text/html')
	    self.end_headers()
	    self.wfile.write(cmd)
	    self.wfile.write('</br>')
	    self.wfile.write(args)
	    return
	except HTTPException:
	    self.send_error(404,'DIE')

    def do_POST(self):
	self.send_error(404, 'DIE')


def main():
    configFiles = [u'/etc/bithead.conf']
    config = ConfigParser()
    config.read(configFiles)

    port = config.getint('http','port')
    Database.loadConfig(config)
    
    try:
	server = HTTPServer(('',port), MyHandler)
	print "Started HTTPServer, listening to port %s" % (port)
	server.serve_forever()
    except KeyboardInterrupt:
	print 'TERM signal recieved, shutting down server'
	server.socket.close()

if __name__=='__main__':
    main()
