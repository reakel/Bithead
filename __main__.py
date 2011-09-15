#!/usr/bin/env python
from main import *
if __name__=='__main__':
    try:
        server = HTTPServer(('',port), MyRequestHandler)
        print "Started HTTPServer, listening to port %s" % (port)
        server.serve_forever()
    except KeyboardInterrupt:
        print 'TERM signal recieved, shutting down server'
        server.socket.close()
