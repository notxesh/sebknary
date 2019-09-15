#!/usr/bin/python3

from os import environ

from dnslib import *

"""
	DNS Response handler

"""

"""
	Load the listening IP address
"""
def getIP():
	try:
		ip = environ['DNS_IP']
		return str(ip)
	except KeyError:
		return "127.0.0.1"

"""
	Load the DNS TTL from the environment,
	if this fails the default ttl will be 60
"""
def getTTL():
	try:
		ttl = environ['DNS_TTL']
		return int(ttl)
	except KeyError:
		return 60

"""
	Load the Domains array to respond too from the environment
"""
def getDomains():
	try:
		domains = environ['DNS_DOMAINS']
		return eval(domains, {'__builtins__': None}, {})
	except KeyError:
		print("[**][DNS][ERR] No domains set in the environment!")
		return []


"""
	Build the actual response too the dns query
"""
def dns_response(data):

	IP = getIP()
	TTL = getTTL()
	domains = getDomains()

	def check_end(dom):
		chk = False
		for d in domains:
			if dom.endswith(d + "."):
				chk = True
				break
		return chk

	request = DNSRecord.parse(data)

	qname = str(request.q.qname)
	qtype = request.q.qtype

	q = DNSRecord(DNSHeader(id=request.header.id, qr=1), q=DNSQuestion(qname, qtype))
	reply = q.reply()

	"""
		Add Randomisation here for domain stuff
	"""

	if (qname in domains) or (check_end(qname)):
		reply.add_answer(RR(qname, QTYPE.A, rdata=A(IP), ttl=TTL))
		"""
		reply.add_answer(RR("", QTYPE.SOA, rdata=SOA("ns1."+qname, 'hostmaster.'+qname, (694201337, 3600, 1800, 604800, 86400)), ttl=TTL))
		reply.add_answer(RR(qname, QTYPE.A, rdata=A(IP), ttl=TTL))
		reply.add_answer(RR(qname, QTYPE.MX, rdata=MX('mail.'+qname), ttl=TTL))
		reply.add_answer(RR(qname, QTYPE.CNAME, rdata=CNAME('crawled.'+qname), ttl=TTL))
		reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(b'Hello World!')))
		"""
	return reply.pack()