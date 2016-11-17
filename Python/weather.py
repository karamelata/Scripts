#!/usr/bin/env python
# Copyright 2016 Dave Machado

import os
import sys
import time
import datetime
import urllib
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from collections import namedtuple
Weather = namedtuple("Weather", "timestamp year month day weekDay condition minTemp maxTemp precipProb precipType humidity windSpeed cloudCover weekSummary")
ROGUE = '-'

API_KEY = open('darkSky_api.txt', 'r').readline()

def openSS(bookName, sheetName):
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open(bookName).worksheet(sheetName)
	return wks

def getWeather(when):
	if (when == 0):
		url='https://api.darksky.net/forecast/' + API_KEY + '/42.6751,-71.4828'
		weatherTime = datetime.datetime.now()
	# If unix timestamp is passed, use Time Machine API call
	else:
		url='https://api.darksky.net/forecast/' + API_KEY + '/42.6751,-71.4828,' + str(when) + '?exclude=flags'
		weatherTime = datetime.datetime.fromtimestamp(when)
	print(weatherTime.strftime('%Y-%m-%d %H:%M:%S'))

	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["timezone"]=="America/New_York":

		if 'summary' not in jsonvalues['daily']['data'][0]:
		    summary = ROGUE
		else:
			summary = jsonvalues['daily']['data'][0]['summary']

		if 'apparentTemperatureMin' not in jsonvalues['daily']['data'][0]:
		    apparentTemperatureMin = ROGUE
		else:
			apparentTemperatureMin = jsonvalues['daily']['data'][0]['apparentTemperatureMin']

		if 'apparentTemperatureMax' not in jsonvalues['daily']['data'][0]:
		    apparentTemperatureMax = ROGUE
		else:
			apparentTemperatureMax = jsonvalues['daily']['data'][0]['apparentTemperatureMax']

		precipProb = jsonvalues['daily']['data'][0]['precipProbability']
		if (precipProb == 0):
		    precipVal = ROGUE
		else:
			precipVal = jsonvalues['daily']['data'][0]['precipType']

		if 'humidity' not in jsonvalues['daily']['data'][0]:
		    humidity = ROGUE
		else:
			humidity = jsonvalues['daily']['data'][0]['humidity']

		if 'windSpeed' not in jsonvalues['daily']['data'][0]:
		    windSpeed = ROGUE
		else:
			windSpeed = jsonvalues['daily']['data'][0]['windSpeed']

		if 'cloudCover' not in jsonvalues['daily']['data'][0]:
		    cloudCover = ROGUE
		else:
			cloudCover = jsonvalues['daily']['data'][0]['cloudCover']

		if (time.strftime("%A") == "Sunday"):
			weekSummary = jsonvalues['daily']['summary']
		else:
			weekSummary = ROGUE

		result = Weather(jsonvalues['currently']['time'],
			weatherTime.strftime("%Y"), weatherTime.strftime("%m"), weatherTime.strftime("%d"), weatherTime.strftime("%a"),
			 summary,
			  apparentTemperatureMin,
			   apparentTemperatureMax,
			    precipProb,
			     precipVal,
			      humidity,
			       windSpeed,
			        cloudCover,
			         weekSummary)
		print result
	else:
		print "Weather API call failed on " + time.strftime("%c")
		sys.exit()
	return result

def main():
	wks = openSS("Weather API", "Current")
	result = getWeather(0)
	wks.append_row(result)

if __name__ == '__main__':
    main()
