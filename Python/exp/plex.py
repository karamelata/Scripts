# !/usr/bin/python
import os
import sys
import urllib
import json
import xlsxwriter

def makeSS():
	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook('Expenses01.xlsx')
	worksheet = workbook.add_worksheet()

	# Some data we want to write to the worksheet.
	expenses = (
	    ['Rent', 1000],
	    ['Gas',   100],
	    ['Food',  300],
	    ['Gym',    50],
	)

	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0

	# Iterate over the data and write it out row by row.
	for item, cost in (expenses):
	    worksheet.write(row, col,     item)
	    worksheet.write(row, col + 1, cost)
	    row += 1

	# Write a total using a formula.
	worksheet.write(row, 0, 'Total')
	worksheet.write(row, 1, '=SUM(B1:B4)')

	workbook.close()

def getMovie(title):
	url='http://www.omdbapi.com/?y=&plot=short&r=json&tomatoes=true&t='+str(title)
	response = urllib.urlopen(url).read()
	jsonvalues = json.loads(response)
	if jsonvalues["Response"]=="True":
		imdbrating = jsonvalues['imdbRating']
		print title + " - " + imdbrating
		for key, value in jsonvalues.items():
			print key + " - " + value
	else:
		print "Movie could not be found!"
		sys.exit()

root='/Users/Dave/Github/Scripts/Python/exp/testDir'
dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
for x in range(len(dirlist)):
	title = dirlist[x]
	title = title.replace('', '')[:-7]
	print title
	getMovie(title)

