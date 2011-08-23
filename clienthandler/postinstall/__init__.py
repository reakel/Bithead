from clienthandler import ClientHandler
from os import system


def dec2mac(dec):
    """
    Convert long integer 'dec' to mac address formatted like '00:00:00:00:00:00'
    """
    h = "%x" % dec
    if (len(h) > 12): 
	raise ClientHandler.Error(1001,"Decimal number too large")
    h = "0"*(12-len(h)) + h
    ret = [ h[i:(i+2)] for i in range(0,12,2) ] 
    return ":".join(ret)



class Postinstall(ClientHandler):
    #disse to variablene blir static
    knr_in_DB = False
    knr = None
    
    def __init__(self,addr,args,db): #constructor
        super(Postinstall,self).__init__(addr,args,db)
        self.knr_in_DB = False
        self.knr = None
 
    def getResponse(self):
        self.mac = dec2mac(self.args['client']['id']) 
        self.fetchKnr()
        if not self.knr: 
            raise ClientHandler.Error(1001,'CompID not found in the database.')
        self.knr_in_DB = True
        puppetca_cmd = "puppetca -c" + " " + self.knr + ".felles.ntnu.no"
        #system(puppetca_cmd)
        return { 'status': '0', 'CompID': self.knr }        

    def fetchKnr(self):
	print self.mac
	self.knr = "k2202"
	return
	computerDB = open('/usr/local/share/bithead/database/computers_db', 'r') # TODO: get file path from config
        compDB = computerDB.readlines()
        computerDB.close()
        for computer in compDB:
            compList = computer.split(';')
            if( compList[2] == self.mac ):
                self.knr = compList[1]
                break
    
    def doPostProcessing(self):
            if not self.knr_in_DB:
                #Computer was not authenticated in getResponse(), exit.
                return
	    self.printLog("Entering postprocessing")
            pre = "ssh -o StrictHostKeyChecking=no root@" + self.addr
            #Preparing cmds
            cmds = []
            cmds.append(pre + " \'domainjoin-cli setname " + self.knr + "'")
            cmds.append("echo \'" + Postinstall.adpassword + "\' | " + pre + " \'xargs domainjoin-cli felles.ntnu.no " + Postinstall.aduser + "\'")
            cmds.append(pre + " \'/root/postinstall/lwreg\'")
            cmds.append(pre + " \'reboot\'")
            #Execute cmds and print to log
            for cmd in cmds:
                self.printLog(cmd)
                system(cmd)
    
    @staticmethod
    def loadConfig(config):
	section = 'postinstall'
	Postinstall.adpassword = config.get(section, 'adpassword')
	Postinstall.aduser = config.get(section, 'aduser')
