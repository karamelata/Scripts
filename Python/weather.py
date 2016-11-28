#!/usr/bin/env python
# Copyright 2016 Dave Machado

import os
import sys
import platform
import time
import datetime
import urllib
import json
from geopy.geocoders import Nominatim

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import namedtuple

ONE_DAY = 86400
DEFAULT_COOR = "42.6751,-71.4828"
LOCATION_COOR = "NULL"
LOCATION_INFO = "NULL"

if len(sys.argv) > 1:
	FLAG_CALL = True
else:
	FLAG_CALL = False

API_KEY = open('darkSky_api.txt', 'r').readline()

def clearScreen():
	if (platform.system() == "Windows"):
		os.system('cls')
	else:
		os.system('clear')

def pressKeyToContinue():
	raw_input("\nPress Enter to continue...")

def openSS(bookName, sheetName):
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open(bookName).worksheet(sheetName)
	return wks

def getCoordinates():
	geolocator = Nominatim()
	zipStr = str(raw_input("\nNew location: "))
	if len(zipStr) < 5:
		# Python does not read leading zeros, so pad an extra '0'
		# if x < 5 (length of zip codes)
		zipStr.zfill(5)
	zipStr += " United States"
	#location = geolocator.reverse("42.6751,-71.4828")
	location = geolocator.geocode(zipStr)
	x = str(location.latitude)
	y = str(location.longitude)
	z = x + ", " + y
	print("Coordinates: " + z)
	return z

def getLocationInfo(coordinates):
	geolocator = Nominatim()
	location = geolocator.reverse(coordinates)
	return location.address

def getWeatherJSON(when):
	global LOCATION_COOR
	if (when == 0):
		url='https://api.darksky.net/forecast/' + API_KEY + '/' + LOCATION_COOR
	# If unix timestamp is passed, use Time Machine API call
	else:
		url='https://api.darksky.net/forecast/' + API_KEY + '/' + LOCATION_COOR + ',' + str(when) + '?exclude=flags'
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	return jsonvalues

def getWeather(when):
	jsonvalues = getWeatherJSON(when)
	if when == 0:
		weatherTime = datetime.datetime.now()
	else:
		weatherTime = datetime.datetime.fromtimestamp(when)

	if 'timezone' in jsonvalues:
		print("---- Weather for " + weatherTime.strftime('%B %d, %Y (%a)') + " ----")

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
			
		if 'precipProbability' not in jsonvalues['daily']['data'][0]:
		    precipProbability = ROGUE
		else:
			precipProbability = jsonvalues['daily']['data'][0]['precipProbability']

		if ('precipType' not in jsonvalues['daily']['data'][0]) or (precipProbability == 0):
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

		if 'summary' in jsonvalues['daily']:
			weekSummary = jsonvalues['daily']['summary']
		else:
			weekSummary = ROGUE

		result = Weather(jsonvalues['currently']['time'],
			weatherTime.strftime("%Y"), weatherTime.strftime("%m"), weatherTime.strftime("%d"), weatherTime.strftime("%a"),
			 summary,
			  apparentTemperatureMin,
			   apparentTemperatureMax,
			    precipProbability,
			     precipVal,
			      humidity,
			       windSpeed,
			        cloudCover,
			         weekSummary)
	else:
		print "Weather API call failed on " + time.strftime("%c")
		sys.exit()
	return result

def printReport(result):
	print("Summary: " + str(result[5]))
	print("Low: " + str(result[6]))
	print("High: " + str(result[7]))
	# if precipProb > 0
	if(result[8] > 0):
		print("Chance of " + str(result[9]) + ": " + str(result[8]))
	if not FLAG_CALL:
		pressKeyToContinue()

def getInteractiveChoice():
	global LOCATION_COOR
	global LOCATION_INFO
	while True:
		clearScreen()
		print("-- WEATHER DATA --")
		print("Location: " + LOCATION_INFO + ' (' + LOCATION_COOR + ')')
		print("Please choose from the following options:")
		print("(1) Today")
		print("(2) Tomorrow")
		print("(3) Yesterday")
		print("(4) Weather from Time Machine")
		print("(5) Change Location")
		print("(0) Quit")
		try:
			choice = int(raw_input("Choice: "))
		except ValueError:
			continue
		if choice < 0 or choice > 5:
			continue
		else:
			return choice

def userMode(choice):
	global LOCATION_COOR
	global LOCATION_INFO
	while True:
		if choice == -1:
			choice = getInteractiveChoice()
		if choice == 0:
			sys.exit()
		if choice == 1:
			result = getWeather(0)
			timestamp = datetime.datetime.now()
			printReport(result)
		if choice == 2:
			timestamp = int(time.time())
			timestamp += ONE_DAY
			result = getWeather(timestamp)
			printReport(result)
		if choice == 3:
			timestamp = int(time.time())
			timestamp -= ONE_DAY
			result = getWeather(timestamp)
			printReport(result)
		if choice == 4:
			print("-- Time Machine Weather Report --")
			dateStr = raw_input("MM/DD/YYYY: ")
			try:
				dateStr += " 11:00PM"
				timestamp = datetime.datetime.strptime(dateStr, "%m/%d/%Y %I:%M%p")
				unixTime = time.mktime(timestamp.timetuple())
			except ValueError:
				raise ValueError("Incorrect data format, should be MM/DD/YYYY")
			result = getWeather(int(unixTime))
			printReport(result)

		if choice == 5:
			weatherCoordinates = getCoordinates()
			weatherLocation = getLocationInfo(weatherCoordinates)
			LOCATION_COOR = weatherCoordinates
			LOCATION_INFO = weatherLocation
		# If called with CLI flag, no need to loop (not interactive mode)
		if FLAG_CALL:
			sys.exit()
		choice = -1

def callHelp():
	print("-- WEATHER DATA --")
	print("call " + str(sys.argv[0]) + " -X: ")
	print("-a    : auto-add daily weather to Google Sheet")
	print("-i    : Interactive Mode")
	print("-n    : Weather for today")
	print("-t    : Weather for tomorrow")
	print("-y    : Weather for yesterday")
	print("-m    : Time Machine weather")
	print("-h    : Call this help menu again")
	sys.exit()

def autoMode():
	wks = openSS("Weather API", "Current")
	result = getWeather(0)
	print(result)
	wks.append_row(result)

def main():
	global LOCATION_COOR
	global LOCATION_INFO
	LOCATION_COOR = DEFAULT_COOR
	LOCATION_INFO = getLocationInfo(LOCATION_COOR)
	if FLAG_CALL:
		mode = str(sys.argv[1])
		if mode == '-a':
			autoMode()
		if mode == '-i':
			userMode(-1)
		if mode == '-n':
			userMode(1)
		if mode == '-t':
			userMode(2)
		if mode == '-y':
			userMode(3)
		if mode == '-m':
			userMode(4)
		if mode == '-h' or mode == "-help":
			callHelp()
	else:
		userMode(-1)

Weather = namedtuple("Weather", "timestamp year month day weekDay condition minTemp maxTemp precipProb precipType humidity windSpeed cloudCover weekSummary")
ROGUE = '-'
ONE_DAY = 86400
API_KEY = open('darkSky_api.txt', 'r').readline()

if __name__ == '__main__':
    main()

