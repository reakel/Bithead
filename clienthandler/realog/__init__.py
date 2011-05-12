#!/usr/bin/env python
from clienthandler import ClientHandler

class Realog(ClientHandler):
    def getRespone(self):
	#Kjøre getResponse i parent klassen
        super(Pubkey,self).getResponse()
	#Initialisere db objekt
        db = db.getCursor()
	# Tar vi i mot argumenter som dict
	args = self.args

	maskinnavn = args["maskinnavn"]
	brukernavn = args["brukernavn"]
	innloggingstid = args["innloggingstid"]
	utloggingstid = args["utloggingstid"]
	# Nåværende tid kan kanskje brukes i framtiden for å sikre mot nedtid på serveren

	db.query("""INSERT INTO Comp_usage(CompID, User, LoginTime, LogoutTime)
			VALUES(%s, %s, %s, %s)
			UPDATE Computers SET OS='ubuntu' WHERE CompID LIKE %s""" %(maskinavn, brukernavn, innloggingstid, utloggingstid, maskinnavn))

        # Skal returnere dict
