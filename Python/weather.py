#!/usr/bin/env python
# Copyright 2016 Dave Machado

import os
import sys
import time
import urllib
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from collections import namedtuple
Weather = namedtuple("Weather", "year month day weekDay condition minTemp maxTemp precipProb precipType humidity windSpeed cloudCover weekSummary")
ROGUE = '-'

API_KEY = open('darkSky_api.txt', 'r').readline()

def openSS(sheetName):
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open(sheetName).sheet1
	return wks

def getWeather():
	url='https://api.darksky.net/forecast/' + API_KEY + '/42.6751,-71.4828'
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["timezone"]=="America/New_York":
		if (time.strftime("%A") == "Sunday"):
			weekSummary = jsonvalues['daily']['summary']
		else:
			weekSummary = ROGUE
		result = Weather(time.strftime("%Y"), time.strftime("%B"), time.strftime("%d"), time.strftime("%A"), 
			 jsonvalues['daily']['data'][0]['summary'],
			 jsonvalues['daily']['data'][0]['apparentTemperatureMin'],
			  jsonvalues['daily']['data'][0]['apparentTemperatureMax'],
			   jsonvalues['daily']['data'][0]['precipProbability'],
			    jsonvalues['daily']['data'][0]['precipType'],
			     jsonvalues['daily']['data'][0]['humidity'],
			      jsonvalues['daily']['data'][0]['windSpeed'],
			       jsonvalues['daily']['data'][0]['cloudCover'],
			        weekSummary)
		print result
	else:
		print "Weather API call failed on " + time.strftime("%c")
		sys.exit()
	return result

def main():
	wks = openSS("Weather API")
	result = getWeather()
	wks.append_row(result)

if __name__ == '__main__':
    main()
