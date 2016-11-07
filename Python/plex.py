# !/usr/bin/python
import os
import sys
import urllib
import json
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from collections import namedtuple
Movie = namedtuple("Movie", "title director genre time rating imdbMeter rottenMeter rottenUserMeter releaseYear boxOffice plot imdbURL rottenURL")
ROGUE = '-'
reload(sys)  
sys.setdefaultencoding('utf8')

class Logger:
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("output.log", "a")

    def __init__(self, fileName):
        self.terminal = sys.stdout
        self.log = open(fileName, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

def openSS(sheetName):
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open(sheetName).sheet1
	return wks

def writeToSS(wks, movie):
	title = movie[0]
	apiResponse = movie[1]
	try:
		cell = wks.find(title)
		if(cell.col == 1):
			print "Already in workbook: " + title + "\n"
			return
	except gspread.exceptions.CellNotFound:
		pass
	if apiResponse is ROGUE:
		print "Adding raw title to workbook..."
	else:
		print "Adding to workbook..."
	wks.append_row(movie)
	print title + " added." + "\n"

def getMovie(title, year):
	url='http://www.omdbapi.com/?plot=short&r=json&tomatoes=true&t='+str(title)+'&y='+str(year)
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["Response"]=="True":
		title = jsonvalues['Title']
		director = jsonvalues['Director']
		genre = jsonvalues['Genre']
		time = jsonvalues['Runtime']
		# Remove all whitespace and last 3 characters from string (used to chop 'min' off of time)
		time = ''.join(time.split())[:-3]
		rated = jsonvalues['Rated']
		imdb = jsonvalues['imdbRating']
		tomatoScore = jsonvalues['tomatoMeter']
		tomatoUser = jsonvalues['tomatoUserMeter']
		year = jsonvalues['Year']
		boxOffice = jsonvalues['BoxOffice']
		plot = jsonvalues['Plot']
		imdbURL = 'http://www.imdb.com/title/' + jsonvalues['imdbID']
		tomatoURL = jsonvalues['tomatoURL']
		movie = Movie(title, director, genre, time, rated, imdb, tomatoScore, tomatoUser, year, boxOffice, plot, imdbURL, tomatoURL)
		print title + " processed."
	else:
		movie = Movie(title, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE)
		print title + " failed!"
	return movie

def main():
	if len(sys.argv) > 1:
		root = str(sys.argv[1])
	else:
		print "Invalid file path!"
		sys.exit()

	#sys.stdout = Logger("plex-data.log")
	worksheet = openSS("Plex Data")

	dirlist = []
	for item in os.listdir(root):
		dirlist.append(item)
	numOfDir = len(dirlist)
	
	for x in range(numOfDir):
		title = dirlist[x][:-7]
		year = (dirlist[x][-5:])[:-1]
		print str(x+1) + "/" + str(numOfDir)
		print  "Processing " + title + "..."
		movie = getMovie(title, year)
		sys.stdout.flush()
		# Reauth every 100 iterations
		if(x % 100 == 0):
			worksheet = openSS("Plex Data")
		writeToSS(worksheet, movie)

if __name__ == '__main__':
	start_time = time.time()
	print (time.strftime("%m/%d/%Y")) + " " + (time.strftime("%H:%M:%S")) + "\n"
	main()
	print("Execution Time: %s seconds" % (time.time() - start_time))
