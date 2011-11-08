#!/usr/bin/env python
from sys import stdout
from datetime import datetime
import logging
class Logable(object):
    TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self,**kwargs):
	self.logName = kwargs.get('name') or self.__class__.__name__
	self.logger = logging.getLogger(name=self.logName)

    def printLog(self,str, *args, **kwargs):
	extra = {}
	if kwargs.get('extra'):
	    kwargs['extra'].update(extra)
	else:
	    kwargs['extra'] = extra
	self.logger.info(str,*args, **kwargs)


