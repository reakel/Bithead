#!/usr/bin/env python
"""
Common library for Bithead clients
"""
from urllib import urlencode, urlopen, quote
from urlparse import unquote
import json
import platform
import uuid


# TODO: get these values from config
proto = "http"
host = "curie.nt.ntnu.no"
port = 7070
addr = "%s://%s:%i/" % (proto, host, port)

class RequestError(Exception):
    pass

def sendRequest(target,**kwargs):
    """
    Send request to server module designated by 'target' (i.e. 'Realog') accepts parameters as dict.
    Throws exceptions on http errors or failure to parse json
    """
    un = getInfo()
    kwargs["client"] = getInfo()
    kwargs["os"] = un['system']
    kwargs['compid'] = un[1]
    print kwargs
    posts = json.dumps(kwargs)
    posts=quote(posts)
    url = addr + target
    fh = urlopen(url, data=posts)
    ret = json.load(fh)
    fh.close()
    status = int(ret.get('status'))
    print ret
    if status is None or status != 0:
	raise RequestError("Request error: " + str(ret.get('errormessage')))
    return ret

def getInfo():
    """
    Returns info about the system in a dict.
    system (os), hostname, release (os), version (os), machine (architecture), processor and id (mac)
    """
    keys = ['system','hostname','release','version','machine','processor']
    ret = dict(zip(keys,platform.uname()))
    ret['id'] = uuid.getnode()
    return ret


