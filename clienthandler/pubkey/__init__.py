from clienthandler import ClientHandler

class Pubkey(ClientHandler):
    @staticmethod
    def loadConfig(config):
	section = 'pubkey'
	Pubkey.key = config.get(section,'key')

    def getResponse(self):
	super(Pubkey,self).getResponse()
	if not self.authConn(): raise ClientHandler.Error(1,'')
	return { "key": Pubkey.key }

    def authConn(self):
	return False 

