#!/usr/bin/python3

from os import environ
from threading import Thread
from datetime import datetime
import socketserver as SocketServer

try:
	from .nameserver import TCPRequestHandler, UDPRequestHandler 
except:
	from nameserver import TCPRequestHandler, UDPRequestHandler


"""
	Get the interface to run flask on
"""
def dnsHost():
	try:
		ip = environ['DNS_IP']
		return str(ip)
	except KeyError:
		return "127.0.0.1"

"""
	Get the port to run flask on
"""
def dnsPort():
	try:
		port = environ['DNS_PORT']
		return int(port)
	except KeyError:
		return 53

"""
	Basic script to run the nameserver
"""

class Nameserver(Thread):
	def __init__(self):
		Thread.__init__(self)
		IP = dnsHost()
		PORT = dnsPort()
		self.servers = {
			"UDP": SocketServer.ThreadingUDPServer((IP, PORT), UDPRequestHandler),
			"TCP": SocketServer.ThreadingTCPServer((IP, PORT), TCPRequestHandler)
		}
		self.IP = IP
		self.PORT = PORT
		self.workers = []

	def run(self):
		print(f"[*][DNS] Starting Nameserver at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} ")
		for name, s in self.servers.items():
			try:
				thread = Thread(target=s.serve_forever)
				thread.daemon = True
				thread.setName('DNS-'+name)
				thread.start()
				self.workers.append(thread)
				print(f"[*][DNS] Started {name} listener on {str(self.IP)}:{str(self.PORT)}")
			except:
				print(f"[**][DNS][ERR] Failed to start {name} listener on {str(self.IP)}:{str(self.PORT)}")
