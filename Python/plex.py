# !/usr/bin/python
# $ plex.py [PATH_TO_MOVIES] [-f]*
import os
import sys
import urllib
import json
import time
import urllib.request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import namedtuple
existing_entries = []
Movie = namedtuple(
    "Movie", "title director genre time rating imdbMeter rottenMeter rottenUserMeter tomatoConsensus releaseYear boxOffice plot imdbURL rottenURL poster")
ROGUE = '-'
add_count = 0
skip_count = 0
# reload(sys)
# sys.setdefaultencoding('utf8')
KEY_FILE = "/home/dave/keys/gs_client.json"
BOOK_NAME = "Plex Data"


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
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


def openSS(book_name):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE, scope)
    gc = gspread.authorize(credentials)
    wks = gc.open(book_name).sheet1
    get_existing_entries(wks)
    return wks


def get_existing_entries(wks):
    global existing_entries
    existing_entries = wks.col_values(1)
    existing_entries.pop(0)     # remove header ("Movie Title") from list
    return


def writeToSS(wks, movie):
    global add_count
    global skip_count
    global existing_entries
    title = movie[0]
    api_response = movie[1]
    try:
        if title in existing_entries:
            print("Already in workbook: " + title + "\n")
            skip_count += 1
            return
    except gspread.exceptions.CellNotFound:
        pass
    if api_response is ROGUE:
        print("Adding raw title to workbook...")
    else:
        print("Adding to workbook...")
    wks.append_row(movie)
    add_count += 1
    existing_entries.append(title)
    print(title + " added." + "\n")


def process_movie(title, year):
    url = 'http://www.omdbapi.com/?plot=short&r=json&tomatoes=true&t=' + \
        str(title) + '&y=' + str(year)
    url = url.replace(' ', "%20")
    print(url)

    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    response = urllib.request.urlopen(req).read().decode('utf-8')
    jsonvalues = json.loads(response)
    if jsonvalues["Response"] == "True":
        title = jsonvalues['Title']
        director = jsonvalues['Director']
        genre = jsonvalues['Genre']
        time = jsonvalues['Runtime']
        # Remove all whitespace and last 3 characters from string (used to chop
        # 'min' off of time)
        time = ''.join(time.split())[:-3]
        rated = jsonvalues['Rated']
        imdb = jsonvalues['imdbRating']
        tomatoScore = jsonvalues['tomatoMeter']
        tomatoUser = jsonvalues['tomatoUserMeter']
        tomatoSummary = jsonvalues['tomatoConsensus']
        year = jsonvalues['Year']
        boxOffice = jsonvalues['BoxOffice']
        plot = jsonvalues['Plot']
        imdbURL = 'http://www.imdb.com/title/' + jsonvalues['imdbID']
        tomatoURL = jsonvalues['tomatoURL']
        poster = jsonvalues['Poster']
        movie = Movie(title, director, genre, time, rated, imdb, tomatoScore,
                      tomatoUser, tomatoSummary, year, boxOffice, plot,
                      imdbURL, tomatoURL, poster)
        for e in movie:
            if e == "N/A":
                e = ROGUE
        print(title + " processed.")
    else:
        movie = Movie(title, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE,
                      ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE, ROGUE)
        print(title + " failed!")
    return movie


def main():
    if len(sys.argv) > 1:
        root = str(sys.argv[1])
    else:
        print("Invalid file path!")
        sys.exit()

    # sys.stdout = Logger("plex-data.log")
    worksheet = openSS(BOOK_NAME)

    dirlist = []
    if len(sys.argv) >= 2 and sys.argv[2] == "-f":
        #   it's a file listing all the movies
        filen = open(root, "r")
        for line in filen:
            dirlist.append(line)
        numOfDir = len(dirlist)
    else:
        #  the passed-in argument is a directory
        for item in sorted(os.listdir(root)):
            dirlist.append(item)
        numOfDir = len(dirlist)

    for x in range(numOfDir):
        title = dirlist[x][:-7]  # remove year from dir name
        year = (dirlist[x][-5:])[:-1]  # remove title from dir name
        print(str(x + 1) + "/" + str(numOfDir))
        print("Processing " + title + "...")
        movie = process_movie(title, year)
        sys.stdout.flush()
        # Reauth every 50 iterations
        if(add_count % 50 == 0):
            worksheet = openSS(BOOK_NAME)
        writeToSS(worksheet, movie)


if __name__ == '__main__':
    start_time = time.time()
    print((time.strftime("%m/%d/%Y")) + " " +
          (time.strftime("%H:%M:%S")) + "\n")
    main()
    print("%s added, %s skipped." % (str(add_count), str(skip_count)))
    print("Execution Time: %s seconds" % (time.time() - start_time))
