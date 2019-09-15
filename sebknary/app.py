#!/usr/bin/python3

import sys
import time
from os import environ
from datetime import datetime

from sebknary.dns import Nameserver
from sebknary.http import HTTPServer


def runKnary():
	def getDNSEnabled():
		return True if environ.get('DNS') else False
	def getHTTPEnabled():
		return True if environ.get('HTTP') else False

	DNS = getDNSEnabled()
	HTTP = getHTTPEnabled()

	servers = {"DNS": None, "HTTP": None}

	if getDNSEnabled():
		servers['DNS'] = Nameserver()
		servers['DNS'].run()
	if getHTTPEnabled():
		servers['HTTP'] = HTTPServer()
		servers['HTTP'].run()
	if (getDNSEnabled() == False) and (getHTTPEnabled() == False):
		print("[**][SYSTEM][ERR] Please enable your knary modules!")
		return None

	try:
		while 1:
			time.sleep(1)
			sys.stderr.flush()
			sys.stdout.flush()
	except KeyboardInterrupt:
		pass
	finally:
		if getDNSEnabled():
			print(f"[*][DNS] Finished shutdown at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} ")
		if getHTTPEnabled():
			print(f"[*][HTTP] Finished shutdown at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} ")

	print("[**][SYSTEM] Exiting...")
