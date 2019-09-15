#!/usr/bin/python3

try:
	from .handlers import TCPRequestHandler, UDPRequestHandler
except:
	from handlers import TCPRequestHandler, UDPRequestHandler

