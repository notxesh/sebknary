#!/usr/bin/python3


"""
	
	Flask implementation for the HTTP Server
	Overall this is more noisy and doesnt just die when you tell it too

"""


import logging
from os import environ
from threading import Thread
from datetime import datetime
from flask import Flask, request


try:
	from .logger import logger
except:
	from logger import logger

"""
	Get the interface to run flask on
"""
def getHost():
	try:
		ip = environ['HTTP_IP']
		return str(ip)
	except KeyError:
		return "127.0.0.1"

"""
	Get the port to run flask on
"""
def getPort():
	try:
		ip = environ['HTTP_IP']
		return str(ip)
	except KeyError:
		return 5000


app = Flask(__name__)

# Disable normal flask logs
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True
#log.setLevel(logging.ERROR)


@app.before_request
def httplogger():

	req = {}

	req['ip'] = request.remote_addr
	
	if request.headers.getlist('X-Forwarded-For'):
		req['ip'] = str(request.headers.getlist('X-Forwarded-For')[0]).strip()

	req['host'] = str(request.host.split(':')[0]).strip()
	req['path'] = str(request.path).strip()
	req['method'] = str(request.method).strip()
	req['headers'] = request.headers
	req['args'] = str(request.query_string, 'utf-8').strip()
	req['data'] = str(request.data, 'utf-8').strip()
	req['url'] = str(request.url).strip()

	log = logger(req)
	log.start()

@app.route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
def index():
	return ""

@app.route("/<path:path>", methods=["GET", "POST", "HEAD", "OPTIONS"])
def all(path):
	return ""

class HTTPServer(Thread):
	def __init__(self):
		Thread.__init__(self)
		global app
		self.HOST = getHost()
		self.PORT = getPort()
		app.host = self.HOST
		app.port = self.PORT
		self.app = Thread(target=app.run)
		
	def run(self):
		self.app.start()
		print(f"[*][HTTP] Started Listener at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

