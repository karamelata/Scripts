#!/usr/bin/env python3
# Copyright 2017 Dave Machado

import os
import sys
import platform
import time
import datetime
import urllib.request
import json
import pymysql
from geopy.geocoders import Nominatim

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import namedtuple

Weather = namedtuple("Weather", "timestamp year month day weekDay condition\
 	minTemp maxTemp precipProb precipType humidity windSpeed cloudCover weekSummary")

apiKeyFile = '/Users/Dave/keys/darkSky_api.txt'
sqlPswdFile = '/Users/Dave/keys/sql_pswd.txt'
gsJSONFile = '/Users/Dave/keys/gs_client.json'
ROGUE = None
ONE_DAY = 86400
DEFAULT_COOR = "42.6751,-71.4828"
LOCATION_COOR = "NULL"
LOCATION_INFO = "NULL"


API_KEY = open(apiKeyFile, 'r').readline()
SQL_PSWD = open(sqlPswdFile, 'r').readline()[:-1]

db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     passwd=SQL_PSWD,
                     db="weather",
                     charset='utf8')

cur = db.cursor()

if len(sys.argv) > 1:
    FLAG_CALL = True
else:
    FLAG_CALL = False


def cleanup(exit_code=0):
    db.commit()
    cur.close()
    db.close()
    sys.exit(exit_code)


def clearScreen():
    if (platform.system() == "Windows"):
        os.system('cls')
    else:
        os.system('clear')


def pressKeyToContinue():
    input("\nPress Enter to continue...")


def openSS(bookName, sheetName):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        gsJSONFile, scope)
    gc = gspread.authorize(credentials)
    wks = gc.open(bookName).worksheet(sheetName)
    return wks


def check_in_table(id_to_check, table_name):
    sql = "SELECT * FROM %s WHERE `id`=%s" % (
        table_name, str(id_to_check))
    cur.execute(sql)
    return cur.fetchone()


def add_sql(results, table_name):
    sql = """
	    CREATE TABLE IF NOT EXISTS %s
	    (
	      id              	int unsigned NOT NULL,
	      added         	datetime NOT NULL,
	      year         		int unsigned NOT NULL,
	      month         	int unsigned NOT NULL,
	      day         		int unsigned NOT NULL,
	      week_day			varchar(16) NOT NULL,
	      summary_day		varchar(255) NOT NULL,
	      temp_min          float(8) NOT NULL,
	      temp_max          float(8) NOT NULL,
	      precip_prob       float(8) NOT NULL,
	      precip_type       varchar(16),
	      humidity          float(8) NOT NULL,
	      wind_speed        float(8) NOT NULL,
	      cloud_cover       float(8),
	      summary_week      varchar(255),
	      PRIMARY KEY     	(id)
	    );
    """ % table_name
    try:
        cur.execute(sql)
    except pymysql.ProgrammingError as e:
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        return False

    if check_in_table(results[0], table_name) is not None:
        print(results[0], "is already in", table_name, "- skipping insert")
        return

    sql = "INSERT INTO " + table_name + \
        " (id, added, year, month, day, week_day, summary_day, temp_min, temp_max, precip_prob, precip_type, humidity, wind_speed, cloud_cover, summary_week) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        timestamp = datetime.datetime.fromtimestamp(
            float(results[0])).strftime('%Y-%m-%d %H:%M:%S')
        args = (results[0], timestamp, results[1], results[2], results[3], results[4], results[5], results[6],
                results[7], results[8], results[9], results[10], results[11], results[12], results[13])
        cur.execute(sql, args)
        print("Added to SQL:", timestamp)
        # print(cur._executed)
    except pymysql.ProgrammingError as e:
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        print(cur._executed)
        cleanup(1)
    except ValueError as e:
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        print(results[0])
        cleanup(1)

    return True


def convert_excel_to_sql(wks, table_name):
    all_dates = wks.get_all_values()[1:]
    count = 1
    day_size = len(all_dates[1])
    total = len(all_dates)
    for day in all_dates:
        for i in range(day_size):
            if day[i] == "None":
                day[i] = None
        print(count, "/", total)
        add_sql(day, table_name)
        count += 1
    cleanup()


def getCoordinates(locationString):
    geolocator = Nominatim()
    if len(locationString) < 5:
        # Python does not read leading zeros, so pad an extra '0'
        # if x < 5 (length of zip codes)
        locationString.zfill(5)
    locationString += " United States"
    #location = geolocator.reverse("42.6751,-71.4828")
    location = geolocator.geocode(locationString)
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
    if (when == 0):
        url = 'https://api.darksky.net/forecast/' + API_KEY + '/' + LOCATION_COOR
    # If unix timestamp is passed, use Time Machine API call
    else:
        url = 'https://api.darksky.net/forecast/' + API_KEY + \
            '/' + LOCATION_COOR + ',' + str(when) + '?exclude=flags'
    response = urllib.request.urlopen(url).read()
    jsonvalues = json.loads(response)
    return jsonvalues


def getWeather(when):
    jsonvalues = getWeatherJSON(when)
    if when == 0:
        weatherTime = datetime.datetime.now()
    else:
        weatherTime = datetime.datetime.fromtimestamp(when)

    if 'timezone' in jsonvalues:

        if 'summary' not in jsonvalues['daily']['data'][0]:
            summary = ROGUE
        else:
            summary = jsonvalues['daily']['data'][0]['summary']

        if 'apparentTemperatureMin' not in jsonvalues['daily']['data'][0]:
            apparentTemperatureMin = ROGUE
        else:
            apparentTemperatureMin = jsonvalues['daily'][
                'data'][0]['apparentTemperatureMin']

        if 'apparentTemperatureMax' not in jsonvalues['daily']['data'][0]:
            apparentTemperatureMax = ROGUE
        else:
            apparentTemperatureMax = jsonvalues['daily'][
                'data'][0]['apparentTemperatureMax']

        if 'precipProbability' not in jsonvalues['daily']['data'][0]:
            precipProbability = ROGUE
        else:
            precipProbability = jsonvalues['daily'][
                'data'][0]['precipProbability']

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

        result = Weather(
            jsonvalues['currently']['time'],
            weatherTime.strftime("%Y"),
            weatherTime.strftime("%m"),
            weatherTime.strftime("%d"),
            weatherTime.strftime("%a"),
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
        print("Weather API call failed on " + time.strftime("%c"))
        cleanup()
    return result


def printReport(result, pauseAfterPrinting):
    weatherTime = datetime.datetime.fromtimestamp(int(result[0]))
    print("---- " + weatherTime.strftime('%m-%d-%Y (%a)') + " ----")
    print("Condition: " + str(result[5]))
    # if precipProb > 0
    if(result[8] > 0):
        print("Chance of " + str(result[9]) + ": " + str(result[8]))
    print("Temp: " + str(int(result[7])) + "/" + str(int(result[6])) + "\n")
    if not FLAG_CALL and pauseAfterPrinting is True:
        pressKeyToContinue()


def getInteractiveChoice():
    while True:
        clearScreen()
        print("-- WEATHER DATA --")
        print("Location: " + LOCATION_INFO + ' (' + LOCATION_COOR + ')')
        print("Please choose from the following options:")
        print("(1) Today")
        print("(2) Tomorrow")
        print("(3) Yesterday")
        print("(4) Weather from Time Machine")
        print("(5) Weekly Report")
        print("(9) Change Location")
        print("(0) Quit")
        try:
            choice = int(input("Choice: "))
        except ValueError:
            continue
        if choice < 0 or choice > 5 and choice != 9:
            continue
        else:
            return choice


def userMode(choice):
    global LOCATION_COOR
    global LOCATION_INFO
    LOCATION_INFO = getLocationInfo(LOCATION_COOR)
    while True:
        if choice == -1:
            choice = getInteractiveChoice()
        if choice == 0:
            cleanup()
        if choice == 1:
            result = getWeather(0)
            timestamp = datetime.datetime.now()
            printReport(result, True)
        if choice == 2:
            timestamp = int(time.time())
            timestamp += ONE_DAY
            result = getWeather(timestamp)
            printReport(result, True)
        if choice == 3:
            timestamp = int(time.time())
            timestamp -= ONE_DAY
            result = getWeather(timestamp)
            printReport(result, True)
        if choice == 4:
            if len(sys.argv) > 2:
                dateStr = str(sys.argv[2])
            else:
                print("-- Time Machine Weather Report --")
                dateStr = input("MM/DD/YYYY: ")
            try:
                dateStr += " 6:00PM"
                timestamp = datetime.datetime.strptime(
                    dateStr, "%m/%d/%Y %I:%M%p")
                unixTime = time.mktime(timestamp.timetuple())
            except ValueError:
                raise ValueError("Incorrect data format, should be MM/DD/YYYY")
            result = getWeather(int(unixTime))
            printReport(result, True)
        if choice == 5:
            clearScreen()
            unixTime = int(time.time())
            result = getWeather(0)
            print("\nThis Week: " + str(result[13]) + "\n")
            printReport(result, False)
            for x in range(6):
                unixTime += ONE_DAY
                result = getWeather(unixTime)
                printReport(result, False)
            if not FLAG_CALL:
                pressKeyToContinue()

        if choice == 9:
            locStr = str(input("\nNew location: "))
            weatherCoordinates = getCoordinates(locStr)
            weatherLocation = getLocationInfo(weatherCoordinates)
            LOCATION_COOR = weatherCoordinates
            LOCATION_INFO = weatherLocation
        # If called with CLI flag, no need to loop (not interactive mode)
        if FLAG_CALL:
            cleanup()
        choice = -1


def callHelp():
    print("-- WEATHER DATA --")
    print("call " + str(sys.argv[0]) + " -X: ")
    print("-a    : auto-add daily weather to Google Sheet")
    print("-n    : Weather for today")
    print("-t    : Weather for tomorrow")
    print("-y    : Weather for yesterday")
    print("-m    : Time Machine weather")
    print("-w    : Weekly Report")
    print("-h    : Call this help menu again")
    cleanup()


def autoMode():
    wks = openSS("Weather API", "Current")
    result = getWeather(0)
    print(result)
    wks.append_row(result)
    add_sql(result, "current")
    #wks = openSS("Weather API", "PastWeather")
    #convert_excel_to_sql(wks, "past")
    cleanup()


def main():
    global LOCATION_COOR
    global FLAG_CALL

    LOCATION_COOR = DEFAULT_COOR
    if FLAG_CALL:
        mode = str(sys.argv[1])
        if mode == '-a':
            autoMode()
        if mode == '-n':
            userMode(1)
        if mode == '-t':
            userMode(2)
        if mode == '-y':
            userMode(3)
        if mode == '-m':
            userMode(4)
        if mode == '-w':
            userMode(5)
        if mode == '-h' or mode == "-help" or mode == "--help":
            callHelp()
        else:
            FLAG_CALL = False
            userMode(-1)
    else:
        userMode(-1)

if __name__ == '__main__':
    main()
