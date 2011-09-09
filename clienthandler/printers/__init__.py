#!/usr/bin/env python
from clienthandler import ClientHandler


class Printers(ClientHandler):
    def getResponse(self):
        super(Printers,self).getResponse()
        args = self.args
        #args should contain:
	#nothing more than default values

        try:
            machine_name = args["client"]["hostname"]
            os = args["client"]["system"]
        except Exception as e:
	    raise Exception(3,'fubar')
	ret = {}
	c = self.db.getCursor()
	c.execute("""SELECT PrinterURI,Room.RoomID as RoomID FROM Computers LEFT JOIN Room ON Computers.RoomID=Room.RoomID WHERE CompID=%s""", (machine_name,))
	(printerURI, roomID) = c.fetchone()
	if printerURI is None: raise Printers.Error(1,'No printer defined')
	ret['printerURI'] = printerURI
	ret['roomID'] = roomID
	ret['status'] = 0
	return ret

    def doPostProcessing(self):
        pass
    
