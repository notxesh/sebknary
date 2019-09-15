#!/usr/bin/python3

from os import environ

import requests
from discord import Embed, Webhook, RequestsWebhookAdapter


def getDiscordHook():
	try:
		webhook = environ['WEBHOOK_DISCORD']
		return webhook
	except:
		print("[**][DISCORD][ERR] Unable to find webhook! please set 'WEBHOOK_DISCORD' in your environment.")
		return ""

def sendMessage(embed):
	whook = Webhook.from_url(getDiscordHook(), adapter=RequestsWebhookAdapter())
	whook.send(embed=embed)

def dnsTrigger(ip, lookup):
	emb = Embed(title="Knary - DNS", description="New knary hit!", color=0x7289DA)
	emb.add_field(name="IP", value=f"` {str(ip)} `", inline=True)
	emb.add_field(name="Lookup", value=f"` {str(lookup)} `", inline=True)
	sendMessage(emb)

def httpTrigger(req):
	
	def formatHeaders(headers):
		hStr = ""
		for k, v in headers.items():
			hStr += f"{k}: {v}\r\n"
		return hStr

	# Begin Embed Creation
	emb = Embed(title=f"Knary - HTTP {req['method']}", description=f"New knary hit on: {req['host']}!", color=0x7289DA)
	emb.add_field(name="URL", value=f"{req['url']}", inline=False)
	emb.add_field(name="IP", value=f"> {str(req['ip'])}", inline=True)
	emb.add_field(name="Path", value=f"> {str(req['path'])}", inline=True)

	if (not (req.get('forwarded') in ('', None))):
		emb.add_field(name="Forwarded-For", value=f"> {str(req['forwarded'])}", inline=True)

	if (not (req['args'] in ("", None))):
		emb.add_field(name="Query", value=f"> {str(req['args'])}")

	if (not (req.get('frag') in ("", None))):
		em.add_field(name="Fragment", value=f"``` {str(req['frag'])} ```", inline=False)

	if (not (req.get('data') in ("", None))):
		emb.add_field(name="Data", value=f"```{str(req['data'])}```", inline=False)

	emb.add_field(name="Headers", value=f"```{formatHeaders(req['headers'])}```", inline=False)
	sendMessage(emb)
