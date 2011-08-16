#!/usr/bin/env python
"""
Common client library for Bithead
"""
from urllib import urlencode, urlopen
import json


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
    args = urlencode(kwargs)
    url = addr + target + '?' + args
    fh = urlopen(url)
    ret = json.load(fh)
    fh.close()
    return ret



