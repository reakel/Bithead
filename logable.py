#!/usr/bin/env python
from sys import stdout
from datetime import datetime
class Logable(object):
    logName = ''
    TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self,**kwargs):
	self.output = kwargs.get('output') or stdout

    def printLog(self,str):
        if self.logName:
            name = self.logName
        else:
            name = self.__class__.__name__
        #print "[" + name + "]", str
	lines = str.split('\n')
	timestr = datetime.now().strftime(Logable.TIMEFORMAT)
	for line in lines:
	    self.output.write("[ %s ] -- [ %s ]  %s\n" % (name, timestr, line))


