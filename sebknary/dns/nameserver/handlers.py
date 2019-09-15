#!/usr/bin/python3

from datetime import datetime
import sys
import time
import traceback
import binascii
import socketserver as SocketServer

from dnslib import *

try:
	from .response import dns_response
	from ..logger import logger
except:
	from response import dns_response


"""
	Default DNS Request handler
"""
class BaseRequestHandler(SocketServer.BaseRequestHandler):

	def get_data(self):
		raise NotImplementedError

	def send_data(self, data):
		raise NotImplementedError

	def handle(self):
		# Log to the console
		#print(f"[+][DNS] {self.__class__.__name__[:3]} request {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')} ({self.client_address[0]}:{self.client_address[1]})")
		try:
			data = self.get_data()
			# Logger Thread
			log = logger(ip=self.client_address[0], data=data)
			log.start()
			# Send response
			self.send_data(dns_response(data))
		except Exception:
			traceback.print_exc(file=sys.stderr)

"""
	Handl TCP DNS Requests
"""
class TCPRequestHandler(BaseRequestHandler):

	def get_data(self):
		data = self.request.recv(8192).strip()
		sz = int(data[:2].hex(), 16)
		if sz < len(data) - 2:
			raise Exception("Wrong size of TCP packet")
		elif sz > len(data) - 2:
			raise Exception("Too big TCP packet")
		return data[2:]

	def send_data(self, data):
		sz = binascii.unhexlify(hex(len(data))[2:].zfill(4))
		return self.request.sendall(sz + data)


"""
	Handle UDP DNS Requests
"""
class UDPRequestHandler(BaseRequestHandler):

	def get_data(self):
		return self.request[0].strip()

	def send_data(self, data):
		return self.request[1].sendto(data, self.client_address)
