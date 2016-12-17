#!/usr/bin/env python
import urllib
import json
import sys

def getUserDataAPI(user):
	url='https://api.github.com/users/'+str(user)
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if ('login' in jsonvalues):
		userName = jsonvalues['name']
		print user + " - " + userName
		for key, value in jsonvalues.items():
			print str(key) + " - " + str(value)
	else:
		print "User could not be found!"

if len(sys.argv) > 1:
	user = str(sys.argv[1])
	getUserDataAPI(user)
else:
	print ("syntax: " + sys.argv[0] + " <username>")
