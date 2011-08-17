from clienthandler import ClientHandler
from os import system

class Postinstall(ClientHandler):
    #disse to variablene blir static
    knr_in_DB = False
    knr = None
    passwd = 'nopass' # TODO: get this from somwhere else
    
    def __init__(self,addr,args,db): #constructor
        super(Postinstall,self).__init__(addr,args,db)
        self.knr_in_DB = False
        self.knr = None
 
    def getResponse(self):
        self.mac = self.args['mac'] # TODO: dict entry 'mac' may not exist. Implement a check.
        self.fetchKnr()
        print self.args['a']
        if not self.knr: 
            raise ClientHandler.Error(1001,'CompID not found in the database.')
        self.knr_in_DB = True
        puppetca_cmd = "puppetca -c" + " " + self.knr + ".felles.ntnu.no"
        #system(puppetca_cmd)
        return { 'status': '0', 'CompID': self.knr }        

    def fetchKnr(self):
        computerDB = open('/usr/local/share/bithead/database/computers_db', 'r')        
        compDB = computerDB.readlines()
        
        for computer in compDB:
            compList = computer.split(';')
            if( compList[2] == self.mac ):
                self.knr = compList[1]
                break
    
    def doPostProcessing(self):
            if not self.knr_in_DB:
                #Computer was not authenticated in getResponse(), exit.
                return
            pre = "ssh -o StrictHostKeyChecking=no root@" + self.addr
            #Preparing cmds
            cmds = []
            cmds.append(pre + " \'domainjoin-cli setname " + self.knr + "'")
            cmds.append("echo \'" + Postinstall.passwd + "\' | " + pre + " \'xargs domainjoin-cli felles.ntnu.no spokelsesadmin\'")
            cmds.append(pre + " \'/root/postinstall/lwreg\'")
            cmds.append(pre + " \'reboot\'")
            #Execute cmds and print to log
            for cmd in cmds:
                self.printLog(cmd)
                #system(cmd)
    
    @staticmethod
    def loadConfig(config):
        #TODO: load AD domain,user and password from config file
        pass
