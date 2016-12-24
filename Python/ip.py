#!/usr/bin/env python
# Copyright 2016 Dave Machado
import urllib
import json
import sys

def getIP(ip):
	url='http://ip-api.com/json/'+str(ip)
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["status"]=="success":
		for key, value in jsonvalues.items():
			print str(key) + ": " + str(value)
	else:
		print jsonvalues


if len(sys.argv) > 1:
	ip = str(sys.argv[1])
	getIP(ip)
else:
	getIP('/')
