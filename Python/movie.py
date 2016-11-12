#!/usr/bin/env python
import urllib
import json
import sys
import os
import platform

def clearScreen():
	if (platform.system() == "Windows"):
		os.system('cls')
	else:
		os.system('clear')

def getMovie(title):
	url='http://www.omdbapi.com/?y=&plot=short&r=json&tomatoes=true&t='+str(title)
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["Response"]=="True":
		clearScreen()
		title = jsonvalues['Title']
		imdbrating = jsonvalues['imdbRating']
		tomatoScore = jsonvalues['tomatoMeter']
		print "--------------------------- " + title + " - " + imdbrating + "," + tomatoScore + " ---------------------------" + "\n"
		for key, value in jsonvalues.items():
			print key + ": " + value
	else:
		print "Movie could not be found!"


if len(sys.argv) > 1:
	title = str(sys.argv[1])
	getMovie(title)
else:
	print ("syntax: " + sys.argv[0] + " <MovieTitle>")
