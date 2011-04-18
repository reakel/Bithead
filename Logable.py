#!/usr/bin/env python

class Logable:
    logName = ''
    def printLog(self,parent):
	if self.logName:
	    name = self.logName
	else:
	    name = self.__class__.__name__
	print "[" + name + "]", str


