#!/usr/bin/env python
import bitheadclient as bhc
from datetime import datetime, timedelta

dt = timedelta(hours=1)
now = datetime.now()
data = {
	'user':"espensb",
	'login_time':str(now-dt),
	'logout_time':str(now),
	'now':str(now),
	}
bhc.sendRequest('realog',**data)
