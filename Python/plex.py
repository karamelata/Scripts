# !/usr/bin/python
import os
import sys
import urllib
import json

import xlsxwriter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from collections import namedtuple
Movie = namedtuple("Movie", "title director genre time rating imdbMeter rottenMeter rottenUserMeter releaseYear boxOffice plot rottenURL")

movieArr = []
goodFile = open("success.txt", "w")
badFile = open("failure.txt", "w")

def writeToSS(movieArr = []):
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
	gc = gspread.authorize(credentials)

	wks = gc.open("Plex").sheet1
	#row = 1
	#NUM_OF_MOVIE_VALUES = 12

	for movie in movieArr:
		#for x in range(NUM_OF_MOVIE_VALUES):
		title = movie[0]
		try:
			wks.find(title)
			print "Skipping: " + title + "\n"
 		except gspread.exceptions.CellNotFound:
			print "Adding: " + title + "\n"
			wks.append_row(movie)
			#wks.update_cell(row, x+1, movie[x])
		#row = row + 1
	wks.close()

def getMovie(title):
	url='http://www.omdbapi.com/?y=&plot=short&r=json&tomatoes=true&t='+str(title)
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["Response"]=="True":
		title = jsonvalues['Title']
		director = jsonvalues['Director']
		genre = jsonvalues['Genre']
		time = jsonvalues['Runtime']
		rated = jsonvalues['Rated']
		imdb = jsonvalues['imdbRating']
		tomatoScore = jsonvalues['tomatoMeter']
		tomatoUser = jsonvalues['tomatoUserMeter']
		year = jsonvalues['Year']
		boxOffice = jsonvalues['BoxOffice']
		plot = jsonvalues['Plot']
		tomatoURL = jsonvalues['tomatoURL']
		movie = Movie(title, director, genre, time, rated, imdb, tomatoScore, tomatoUser, year, boxOffice, plot, tomatoURL)
		movieArr.append(movie)
		print title + " processed." + "\n"
	else:
		print title + " failed!" + "\n"

def main():
	if len(sys.argv) > 1:
		root = str(sys.argv[1])
	else:
		print "Invalid file path!"
		sys.exit()

	dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
	numOfDir = len(dirlist)
	for x in range(numOfDir):
		title = dirlist[x]
		title = title.replace('', '')
		print  str(x+1) + "/" + str(numOfDir) + " Processing " + title + "...\n"
		getMovie(title)
	writeToSS(movieArr)
	goodFile.close()
	badFile.close()

if __name__ == '__main__':
    main()
