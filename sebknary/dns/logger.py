#!/usr/bin/python3

from threading import Thread
from dnslib import DNSRecord
from datetime import datetime

try:
	from sebknary.webhooks import discord_hook
except:
	from webhooks import discord_hook

class logger(Thread):
	def __init__(self, ip, data):
		Thread.__init__(self)
		self.ip = str(ip).strip()
		self.data = DNSRecord.parse(data)
	
	def run(self):
		qname = str(self.data.q.qname).strip()
		discord_hook.dnsTrigger(self.ip, qname)
		print(f"[+][DNS] {self.ip} - {qname} {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')}")
