from clienthandler import ClientHandler
from os import system

class Postinstall(ClientHandler):
    #disse to variablene blir static
    #TODO: deklarer disse i constructor
    knr_in_DB = False
    knr = None
    
    def __init__(self): #constructor
        super(Postinstall,self).__init__()
 
    def getResponse(self):
        self.mac = self.args['mac']
        self.getKnr()
        if not self.knr: 
            raise ClientHandler.Error(1001,'CompID not found in the database.')
        self.knr_in_DB = True
        puppetca_cmd = "puppetca -c" + " " + self.knr + ".felles.ntnu.no"
        #system(puppetca_cmd)
        return { 'status': '0', 'CompID': self.knr }	

    def getKnr(self):
        computerDB = open('/usr/local/share/bithead/database/computers_db', 'r')	
        compDB = computerDB.readlines()
        
        for computer in compDB:
            compList = computer.split(';')
            if( compList[2] == self.mac ):
                self.knr = compList[1]
                break
    
    def doPostProcessing(self):
	    pre = "ssh -o StrictHostKeyChecking=no root@" + self.addr
#	    system(pre + " \'domainjoin-cli setname " + self.knr + "'")
#	    system("echo \'" + Postinstall.passwd + "\' | " + pre + " \'xargs domainjoin-cli felles.ntnu.no spokelsesadmin\'")
#	    system(pre + " \'/root/postinstall/lwreg\'")
#	    system(pre + " \'reboot\'")			
        # Checking commands, printing to log:
	    self.printLog(pre + " \'domainjoin-cli setname " + self.knr + "'")
	    self.printLog("echo \'" + Postinstall.passwd + "\' | " + pre + " \'xargs domainjoin-cli felles.ntnu.no spokelsesadmin\'")
	    self.printLog(pre + " \'/root/postinstall/lwreg\'")
	    self.printLog(pre + " \'reboot\'")			
    
    @staticmethod
    def loadConfig(config):
	#TODO: load AD domain,user and password from config file
	pass

