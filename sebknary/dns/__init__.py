#!/usr/bin/python3

try:
	from .app import Nameserver, dnsHost, dnsPort
except:
	from app import Nameserver, dnsHost, dnsPort
