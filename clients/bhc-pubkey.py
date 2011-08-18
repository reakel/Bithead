#!/usr/bin/env python
import bitheadclient as bhc

res = bhc.sendRequest('pubkey')
key = res['key']
fd = open('/root/.ssh/authorized_keys','a')
with fd:
    fd.write(key + "\n")

