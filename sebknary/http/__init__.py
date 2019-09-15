#!/usr/bin/python3

try:
	from .app import HTTPServer, httpHost, httpPort
except:
	from app import HTTPServer, httpHost, httpPort