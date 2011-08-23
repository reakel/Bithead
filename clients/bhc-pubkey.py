#!/usr/bin/env python
import bitheadclient as bhc
from os import mkdir
from path import exists

res = bhc.sendRequest('pubkey')
key = res['key']
if not exists('/root/.ssh'):
    mkdir('/root/.ssh')
fd = open('/root/.ssh/authorized_keys','a')
with fd:
    fd.write(key + "\n")

