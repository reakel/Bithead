#!/usr/bin/env python

"""
Import this to load config files into the 'config' object
"""

import sys
from ConfigParser import ConfigParser
configFiles = ['/etc/bithead.conf',sys.argv[0]+'/bithead.conf']
config = ConfigParser()
config.read(configFiles)
