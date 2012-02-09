#!/usr/bin/env python

"""
Script for updating /etc/hosts with ips by parsing Puppet fact files
Fact files contain ruby objects serialized as yaml strings
"""

import yaml
from os import chdir, listdir
import re
from datetime import datetime, timedelta

factsdir  = "/var/lib/puppet/yaml/facts"
hostsfile = "/etc/hosts"
expiration_days = 2
server = "curie.nt.ntnu.no"
idstr = "#Bithead ipparser"
hoststr = "%s\t%s\t%s\t" + idstr + "\n"

chdir(factsdir) #Change working directory to Puppet facts dir

files = listdir('.') #get files in facts dir
hosts = []
e = re.compile("^((\w+)(\.\w+)+)\.yaml$")   #Regex that matches the naming convention
					    #For a valid fact file i.e. hostname.domain.yaml
today = datetime.now()
while files:
    file = files.pop()
    res = e.match(file)
    if not res: continue	#file is not a fact file, go to next file
    host = res.group(1)		#hostname.domain
    hostshort = res.group(2)	#hostname
    if host == server: continue #do not parse fact file for this computer
    fd = open(file,'r')		
    lines = fd.readlines()
    fd.close()
    lines.pop(0)
    lines = ''.join(lines)
    lines = lines.replace("!","") #Need to remove '!' for the yaml parser to accept the string.
    host_info = yaml.load(lines)
    expired = today - host_info['expiration']
    if (expired.days > 2): continue
    ipaddress = host_info['values']['ipaddress']
    hosts.append((ipaddress, host, hostshort))


e = re.compile('#Reakel ipparser')
fd = open(hostsfile, 'rw')
lines = fd.readlines()
newlines = []
while lines:
    line = lines.pop(0)
    if line.find(idstr) == -1 and line.find("#Reakel ipparser") == -1:
	newlines.append(line)
lines = newlines

for host in hosts:
     lines.append(hoststr % host)

fd.close()
fd = open(hostsfile,"w")
fd.write(''.join(lines))
fd.close()
