#!/usr/bin/env python

from main import *
import logging
if __name__=='__main__':
    try:
        server = ThreadedHTTPServer(('',port), MyRequestHandler)
	server_thread = threading.Thread(target=server.serve_forever)
	#Exit the server thread when the main thread terminates
	server_thread.setDaemon(True)
	server_thread.start()
        print "Started HTTPServer, listening to port %s" % (port)
        secure_server = ThreadedSecureHTTPServer(('',7071), MyRequestHandler)
	secure_server_thread = threading.Thread(target=secure_server.serve_forever)
	#Exit the server thread when the main thread terminates
	secure_server_thread.setDaemon(True)
	secure_server_thread.start()
        print "Started SecureHTTPServer, listening to port %s" % ('7071')

	while server_thread.isAlive() and secure_server_thread.isAlive():
	    sleep(10)
    except KeyboardInterrupt:
	print 'TERM signal recieved, shutting down server'
    finally:
	try:
	    logging.shutdown()
	except:
	    pass
	try:
	    server.socket.close()
	    server.shutdown()
	except:
	    pass
	try:
	    secure_server.socket.close()
	    secure_server.shutdown()
	except:
	    pass


