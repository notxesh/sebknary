#!/usr/bin/python3

"""
	Vanilla HTTP Handler
	This dies when you tell it too and you can disable the logging
	ezpz so I like this better
"""


import ssl
from os import environ
from threading import Thread
from datetime import datetime
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, quote
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
	from .logger import logger
except:
	from logger import logger


"""
	Get the interface to run flask on
"""
def httpHost():
	try:
		ip = environ['HTTP_IP']
		return str(ip)
	except KeyError:
		return "127.0.0.1"

"""
	Get the port to run flask on
"""
def httpPort():
	try:
		port = environ['HTTP_PORT']
		return int(port)
	except KeyError:
		return 5000

"""
	Check to use HTTPS
"""
def getHTTPS():
	return True if environ.get("HTTP_USE_HTTPS") else False

"""
	Get Key File
"""
def getHTTPSKey():
	return environ.get("HTTPS_KEY")

"""
	Get Certificate File
"""
def getHTTPSCert():
	return environ.get('HTTPS_CERT')


class Handler(BaseHTTPRequestHandler):

	def before_req(function):

		def clean(val, url=False):
			rval = str(val).replace('`', '').strip()
			if url:
				rval = str(val).replace('`', '%60').strip()
				rval = quote(rval, safe='/?&=#%')
			return rval

		def cleanDict(d):
			res = {}
			for n, v in d.items():
				nme = n
				val = v
				if isinstance(nme, str):
					nme = clean(n)
				if isinstance(val, str):
					val = clean(v)
				res[nme] = val
			return res

		def wrapper(self):
			self.send_header('Content-type','text/html')
			self.server_version = "nginx"
			self.sys_version = ""
			
			req = {}
			req['ip'] = str(self.client_address[0])

			headers = cleanDict(self.headers)

			if headers.get('X-Forwarded-For'):
				req['forwarded'] = str(headers.get('X-Forwarded-For')[0]).strip()
			req['host'] = headers.get('Host').split(':')[0]
			req['url'] = f"http://{clean(req['host'], url=True)}{clean(self.path, url=True)}"
			try:
				req['path'] = urlparse(req['url']).path
				req['args'] = urlparse(req['url']).query
				req['frag'] = urlparse(req['url']).fragment
			except:
				pass
			req['method'] = str(self.command)
			req['headers'] = headers

			if (req['method'] == "POST"):
				try:
					clen = int(headers.get('Content-Length'))
					req['data'] = clean(str(self.rfile.read(clen), 'utf-8'), url=True)					
				except:
					pass

			log = logger(req)
			log.start()

			func = function(self)
			return func
		return wrapper

	@before_req
	def do_OPTIONS(self):
		self.send_response(200)
		self.end_headers()

	@before_req
	def do_HEAD(self):
		self.send_response(200)
		self.end_headers()

	@before_req
	def do_POST(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b" ")

	@before_req
	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b" ")

	def log_message(self, format, *args):
		return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

class HTTPServer(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.server = ThreadedHTTPServer((httpHost(), httpPort()), Handler)
		if getHTTPS():
			self.server.socket = ssl.wrap(self.server.socket, keyfile=getHTTPSKey(), certfile=getHTTPSCert(), server_side=True)
		self.handler = Thread(target=self.server.serve_forever)
		self.handler.daemon = True
		self.handler.setName("HTTPServer")

	def run(self):
		self.handler.start()
		print(f"[*][HTTP] Started Listener ({httpHost()}:{str(httpPort())}) at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")


