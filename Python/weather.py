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

ONE_DAY = 86400

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

		if (time.strftime("%A") == "Sunday") and ('summary' in jsonvalues['daily']):
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

def getInteractiveChoice():
	while True:
		clearScreen()
		print("-- WEATHER DATA --")
		print("Please choose from the following options.")
		print("(1) Today's Weather")
		print("(2) Tomorrow's Weather")
		print("(3) Yesterday's Weather")
		print("(4) Past Weather from Time Machine")
		try:
			choice = int(raw_input("Choice: "))
		except ValueError:
			continue
		if choice < 1 or choice > 4:
			continue
		else:
			return choice

def userMode(choice):
	if(choice == 0):
		choice = getInteractiveChoice()
	if choice == 1:
		result = getWeather(0)
		timestamp = datetime.datetime.now()
	if choice == 2:
		timestamp = int(time.time())
		timestamp += ONE_DAY
		result = getWeather(timestamp)
	if choice == 3:
		timestamp = int(time.time())
		timestamp -= ONE_DAY
		result = getWeather(timestamp)
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
	print("Summary: " + str(result[5]))
	print("Low: " + str(result[6]))
	print("High: " + str(result[7]))
	# if precipProb > 0
	if(result[8] > 0):
		print("Chance of " + str(result[9]) + ": " + str(result[8]))


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
	if len(sys.argv) > 1:
		mode = str(sys.argv[1])
		if mode == '-a':
			autoMode()
		if mode == '-i':
			userMode(0)
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
		print "Invalid execution, try \'" + str(sys.argv[0]) + " -help\'"
		sys.exit()

if __name__ == '__main__':
    main()
