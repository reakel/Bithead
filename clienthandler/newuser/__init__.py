from clienthandler import ClientHandler
import subprocess
import re
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
        m = re.search(r"uid=(\d+)\D+?gid=(\d+)", sshreturn)
        if m is None:
            raise ClientHandler.Error(200, "Id not found through ssh")
        uid = m.group(1)
        gid = m.group(2)
        idnums = uid + ":" + gid
        
        try:
            #Creates users home directory 
            subprocess.check_call(["mkdir", userdir])
            #Changes owner and group of users home directory
            subprocess.check_call(["chown", "-R", idnums, userdir])
            #Sets permissions for users home directory
            subprocess.check_call(["chmod", "-R", "700", userdir])
            
            logstring = "Created home directory for %s in %s with uid=%s and gid=%s" % (user, userdir, uid, gid)
            self.printLog(logstring)
            return {"status": 0}
        except CalledProcessError as e: #thrown by subprocess.check_all()
            raise ClientHandler.Error(e.returncode, "Subprocess error: " + e.message)



    @staticmethod
    def loadConfig(config):
        section = "newuser"
        Newuser.userdirs = config.get(section, "userdirs")

    def authUser(self, user):
#SSHe til maskina, autentisere bruker og hente ut uid og gid.
        return True

    def printLog(self, str):
        super(Newuser, self).printLog(str)
