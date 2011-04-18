#!/usr/bin/env python
from NewuserHandler import NewuserHandler
import socket
import sys

try:
    while True:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(("localhost", int(sys.argv[1])))
	server.listen(10)
	socket,addr = server.accept()
	NewuserHandler(socket,addr,("Hello",1,2,3))
except:
    pass
finally:
    server.close()

