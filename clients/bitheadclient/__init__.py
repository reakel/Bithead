#!/usr/bin/env python
"""
Common library for Bithead clients
"""
from urllib import urlencode, urlopen, quote
from urlparse import unquote
import json
import platform


# TODO: get these values from config
proto = "http"
host = "curie.nt.ntnu.no"
port = 7070
addr = "%s://%s:%i/" % (proto, host, port)

def sendRequest(target,**kwargs):
    """
    Send request to server module designated by 'target' (i.e. 'Realog') accepts parameters as dict.
    Throws exceptions on http errors or failure to parse json
    """
    un = getHostInfo()
    kwargs["hostinfo"] = getHostInfo()
    kwargs["os"] = un['system']
    kwargs['compid'] = "k4444" #un[1]
    posts = json.dumps(kwargs)
    posts=quote(posts)
    url = addr + target
    fh = urlopen(url, data=posts)
    ret = json.load(fh)
    fh.close()
    return ret

def getHostInfo():
    keys = ['system','node','release','version','machine','processor']
    ret = dict(zip(keys,platform.uname()))
    return ret


