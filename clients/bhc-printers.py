#!/usr/bin/env python
from bitheadclient import sendRequest
addprinter_cmd = "lpadmin -p %(printer_name)s -E -v %(printer_URI)s -P %(ppdfile)s"
res = sendRequest('printers')
printer_info = res['printer_info']
