#!/usr/bin/env python
import urllib
import json
import sys

def getMovie(title):
	url='http://www.omdbapi.com/?y=&plot=short&r=json&tomatoes=true&t='+str(title)
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["Response"]=="True":
		title = jsonvalues['Title']
		imdbrating = jsonvalues['imdbRating']
		print title + " - " + imdbrating
		for key, value in jsonvalues.items():
			print key + " - " + value
	else:
		print "Movie could not be found!"


if len(sys.argv) > 1:
	title = str(sys.argv[1])
	getMovie(title)
else:
	print ("syntax: " + sys.argv[0] + " <MovieTitle>")
