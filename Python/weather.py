#!/usr/bin/env python
# Copyright 2016 Dave Machado

import os
import sys
import platform
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

def clearScreen():
	if (platform.system() == "Windows"):
		os.system('cls')
	else:
		os.system('clear')

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
		print("---- Weather for " + weatherTime.strftime('%m-%d-%Y') + " ----")
	# If unix timestamp is passed, use Time Machine API call
	else:
		url='https://api.darksky.net/forecast/' + API_KEY + '/42.6751,-71.4828,' + str(when) + '?exclude=flags'
		weatherTime = datetime.datetime.fromtimestamp(when)
		print("---- Weather for " + weatherTime.strftime('%B %d, %Y (%a)') + " ----")

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
	else:
		print "Weather API call failed on " + time.strftime("%c")
		sys.exit()
	return result

def userMode():
	while True:
		clearScreen()
		print("-- WEATHER DATA --")
		print("Please choose from the following options.")
		print("(1) Today's Weather")
		print("(2) Past Weather from Time Machine")
		try:
			choice = int(raw_input("Choice: "))
		except ValueError:
			continue
		if choice < 1 or choice > 2:
			continue
		else:
			break

	if choice == 1:
		result = getWeather(0)
		timestamp = datetime.datetime.now()
	if choice == 2:
		dateStr = raw_input("MM/DD/YYYY: ")
		try:
			dateStr += " 11:00PM"
			timestamp = datetime.datetime.strptime(dateStr, "%m/%d/%Y %I:%M%p")
			unixTime = time.mktime(timestamp.timetuple())
		except ValueError:
			raise ValueError("Incorrect data format, should be MM/DD/YYYY")
		result = getWeather(int(unixTime))
	print("Summary: " + str(result[5]))
	print("Low: " + str(result[6]))
	print("High: " + str(result[7]))
	# If precipProb > 0
	if(result[8] > 0):
		print("Chance of " + str(result[9]) + ": " + str(result[8]))


def callHelp():
	print("-- WEATHER DATA --")
	print("call " + str(sys.argv[0]) + " -X: ")
	print("-a    : auto-add daily weather to Google Sheet")
	print("-i    : Interactive Mode")
	print("-help : Call this help menu again")
	sys.exit()

def autoMode():
	wks = openSS("Weather API", "Current")
	result = getWeather(0)
	print(result)
	wks.append_row(result)

def main():
	if len(sys.argv) > 1:
		mode = str(sys.argv[1])
		if mode == '-help':
			callHelp()
		if mode == '-a':
			autoMode()
		else:
			userMode()
	else:
		print "Invalid execution, try \'" + str(sys.argv[0]) + " -help\'"
		sys.exit()

if __name__ == '__main__':
    main()
