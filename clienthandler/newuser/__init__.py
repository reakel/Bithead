from clienthandler import ClientHandler
import subprocess
import re
class Newuser(ClientHandler):

    def getResponse(self):
        super(Newuser, self).getResponse()
        user = self.args['user']
        userdir = self.userdirs + user
        if not self.authUser(user):
            raise ClientHandler.Error(200, "User is not authorized!")
        try:
            cmd = "ssh root@%s -o StrictHostKeyChecking=no id %s" % (self.addr, user)
            sshreturn = subprocess.check_output(cmd.split(" "))
        except CalledProcessError as e:
            errmsg = "Error when tryin to ssh to client:" + e.returncode + e.output
            raise ClientHandler.Error(200, errmsg)
    
    #Use regexp to get userid and groupid from output from ssh
        m = re.search(r"uid=(\d+)\D+?gid=(\d+)", sshreturn)
        if m is None:
            raise ClientHandler.Error(200, "Id not found through ssh")
        uid = m.group(1)
        gid = m.group(2)
        idnums = uid + ":" + gid
        
        #Creates users home directory 
        if subprocess.check_call(["mkdir", userdir]):
            raise ClientHandler.Error(200, "mkdir error")
        #Changes owner and group of users home directory
        if subprocess.check_call(["chown", "-R", idnums, userdir]):
            raise ClientHandler.Error(200, "chown error")
    #Sets permissions for users home directory
        if subprocess.check_call(["chmod", "-R", "700", userdir]):
            raise ClientHandler.Error(200, "chmod error")
        
        logstring = "Created home directory for %s in %s width uid=%s and gid=%s" % (user, userdir, uid, gid)
        self.printLog(logstring)
        
        return {"status": 0}

    @staticmethod
    def loadConfig(config):
        section = "newuser"
        Newuser.userdirs = config.get(section, "userdirs")

    def authUser(self, user):
#SSHe til maskina, autentisere bruker og hente ut uid og gid.
        return True

    def printLog(self, str):
        super(Newuser, self).printLog(str)
