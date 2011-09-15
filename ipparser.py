#!/usr/bin/env python

"""
Script for updating /etc/hosts with ips by parsing Puppet fact files
"""

import yaml
from os import chdir, listdir
import re

factsdir  = "/var/lib/puppet/yaml/facts"
hostsfile = "/etc/hosts"
server = "curie.nt.ntnu.no"
idstr = "#Bithead ipparser"
hoststr = "%s\t%s\t%s\t" + idstr + "\n"

chdir(factsdir)

files = listdir('.')
hosts = []
e = re.compile("^((\w+)(\.\w+)+)\.yaml$")
remexc = re.compile("^ *!.*$")
while files:
    file = files.pop()
    res = e.match(file)
    if not res: continue
    host = res.group(1)
    hostshort = res.group(2)
    if host == server: continue
    fd = open(file,'r')
    lines = fd.readlines()
    fd.close()
    lines.pop(0)
    lines = ''.join(lines)
    lines = lines.replace("!","")
    host_info = yaml.load(lines)
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
