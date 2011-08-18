from clienthandler import ClientHandler
import subprocess
import re
from os import chmod, mkdir, chown
import os
class Newuser(ClientHandler):

    def getResponse(self):
        super(Newuser, self).getResponse()
        #self.args needs: 'user'
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
	self.printLog(sshreturn)
        m = re.search(r"uid=(\d+)\D+?gid=(\d+)", sshreturn)
        if m is None:
            raise ClientHandler.Error(200, "Id not found through ssh")
        uid = int(m.group(1))
        gid = int(m.group(2))
        
	if os.path.exists(userdir):
	    if not os.path.isdir(userdir):
		raise ClientHandler.Error(userdir + " exists but is not directory")
	else:
	    #Creates users home directory 
	    mkdir(userdir)
	    logstring = "Created home directory for %s in %s with uid=%s and gid=%s" % (user, userdir, uid, gid)
	    self.printLog(logstring)
        #Changes owner and group of users home directory
        chown(userdir,uid,gid)
        #Sets permissions for users home directory
	chmod(userdir,0700)
        
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
