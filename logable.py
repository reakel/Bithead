#!/usr/bin/env python

class Logable(object):
    logName = ''

    def __init__(self):
        pass

    def printLog(self,str):
        if self.logName:
            name = self.logName
        else:
            name = self.__class__.__name__
        print "[" + name + "]", str


