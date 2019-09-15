#!/usr/bin/python3

from datetime import datetime
from threading import Thread

try:
	from sebknary.webhooks import discord_hook
except:
	from webhooks import discord_hook

"""
	sebknary/http/logger.py

		Logs the HTTP Request to discord

		@xesh - 2019
"""

class logger(Thread):
	def __init__(self, request):
		Thread.__init__(self)
		self.request = request

	def run(self):
		discord_hook.httpTrigger(self.request)
		print(f"[+][HTTP] {self.request['ip']} - {self.request['url']} {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')}")
