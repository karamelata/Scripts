import urllib
import json

title = raw_input("Movie Title: ")

url='http://www.omdbapi.com/?t='+str(title)
response = urllib.urlopen(url).read()
jsonvalues = json.loads(response)
if jsonvalues["Response"]=="True":
	imdbrating = jsonvalues['imdbRating']
	print title + " - " + imdbrating
	for key, value in jsonvalues.items():
		print key + " - " + value
else:
	print "Movie could not be found!"