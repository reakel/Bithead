#!/usr/bin/env python

import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
	path = self.path
	cmd,args = path.partition('?')[0::2]
	args = args.split('&')
	self.send_response(200)
	self.send_header('Content-type', 'text/html')
	self.end_headers()
	self.wfile.write(cmd)
	self.wfile.write('</br>')
	self.wfile.write(args)
	return

    def do_POST(self):
	self.send_error(404, 'DIE')


def main():
    try:
	server = HTTPServer(('',7070), MyHandler)
	print 'Started HTTPServer'
	server.serve_forever()
    except KeyboardInterrupt:
	print 'TERM signal recieved, shutting down esrver'
	server.socket.close()

if __name__=='__main__':
    main()
