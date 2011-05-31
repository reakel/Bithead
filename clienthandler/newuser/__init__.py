from clienthandler import ClientHandler
import subprocess
import re
class Newuser(ClientHandler):

    def getResponse(self):
        super(NewUser, self).getResponse()
        user = self.args['user']
        userdir = userdirs + user
        if not authUser():
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
        uid = m.groups(0)
        gid = m.groups(1)
        idmuns = uid +":"+gid
        
        #Creates users home directory 
        if subprocess.check_call(["mkdir", userdir]):
            raise ClientHandler.Error(200, "mkdir error")
        #Changes owner and group of users home directory
        if subprocess.check_call(["chown", idnums, userdir]):
            raise ClientHandler.Error(200, "chown error")
    #Sets permissions for users home directory
        if subprocess.check_call(["chmod", "700", userdir]):
            raise ClientHandler.Error(200, "chmod error")
        
        return {"status": 0}

    @staticmethod
    def loadConfig(config):
        section = "newuser"
        Newuser.userdirs = config.get(section, "userdirs")

    def authUser(self, user):
#SSHe til maskina, autentisere bruker og hente ut uid og gid.
        return True
