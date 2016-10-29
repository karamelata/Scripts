# !/usr/bin/python
import os
import sys
import urllib
import json

if len(sys.argv) > 1:
    ip = str(sys.argv[1])
else:
	print "Invalid IP Address!"
	sys.exit()

url='http://ipinfo.io/'+str(ip)+'/json'
response = urllib.urlopen(url).read()
jsonvalues = json.loads(response)
if (jsonvalues):
    for key, value in jsonvalues.items():
        print key + " - " + value
else:
    print "IP could not be found!"
    sys.exit()

