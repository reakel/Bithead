from clienthandler import ClientHandler
import subprocess
class Newuser(ClientHandler):

    def getResponse(self):
        super(NewUser, self).getResponse()
        user = self.args['user']
        userdir = "/storage/ubuntu10-profiles/" + user
        if authUser():
            try:
                cmd = "ssh root@%s -o StrictHostKeyChecking=no id %s" (self.args, user)
                sshreturn = subprocess.check_output(cmd)
            except CalledProcessError as e:
                raise ClientHandler.Error(errno, Error when tryin to ssh to client: e.returncode e.output)

            #Creates users home directory 
            if subprocess.check_call(["mkdir", userdir])
                raise ClientHandler.Error(200, "mkdir error")
            #Changes owner and group of users home directory
            if subprocess.check_call(["chown", idnums, userdir])
                raise ClientHandler.Error(200, "chown error")
            #Sets permissions for users home directory
            if subprocess.check_call(["chmod", "700", userdir])
                raise ClientHandler.Error(200, "chmod error")
    def authUser(self, user)
#SSHe til maskina, autentisere bruker og hente ut uid og gid.
        return True
