#!/usr/local/bin/python3
from plexapi.server import PlexServer
from getpass import getpass
import pymysql
import sys
import os

FAIL_FLAG = False

pswd = getpass()
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd=pswd,
                     db="plex")

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
plex = PlexServer('http://127.0.0.1:32400', os.environ['PLEX_TOKEN'])

def clean_up():
    cur.close()
    db.close()
    sys.exit(0)

def check_in_table(id_to_check, table_name):
    sql = "SELECT `id`, `plex_id` FROM %s WHERE `plex_id`=%s" % (
        table_name, str(id_to_check))
    cur.execute(sql)
    return cur.fetchone()


def insert_movie(x):
    sql = "INSERT INTO movies (plex_id, title, director, genre, studio, duration_min, duration_ms, rating, score, year, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        genre = ""
        for e in x.genres:
            genre += e.tag + ','
        args = (x.ratingKey, x.titleSort.encode('utf-8'), x.directors[0].tag.encode('utf-8'), genre[:-1], str(
                x.studio), x.duration / 60000, x.duration, str(x.contentRating), x.rating, x.year, x.summary.encode('utf-8'))
        # print(args)
        cur.execute(sql, args)
        # Commit your changes in the database
        print("Inserted: " + x.titleSort)
        db.commit()
    except pymysql.ProgrammingError as e:
        # Rollback in case there is any error
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        FAIL_FLAG = True
        return False
    return True


def update_movies():
    sql = """
    CREATE TABLE IF NOT EXISTS movies
    (
      id              int unsigned NOT NULL auto_increment,
      plex_id         int unsigned NOT NULL,
      title           varchar(255) NOT NULL,
      director        varchar(255) NOT NULL,
      genre           varchar(255) NOT NULL,
      studio          varchar(255) NOT NULL,
      duration_min    int NOT NULL,
      duration_ms     int NOT NULL,
      rating          varchar(255) NOT NULL,
      score           float(8) NOT NULL,
      year            int NOT NULL,
      summary         varchar(1024) NOT NULL,
      PRIMARY KEY     (id)
    );
    """

    try:
        # Execute the SQL command
        cur.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    movies = plex.library.section('Movies')
    for x in movies.all():
        if check_in_table(x.ratingKey, 'movies') is not None:
            continue
        else:
            insert_movie(x)

    if not FAIL_FLAG:
        db.commit()

    # Use all the SQL you like
    # cur.execute("SELECT * FROM movies")
    # print all the first cell of all the rows
    # for row in cur.fetchall():
    #    print(row)

def insert_show(x):
    sql = "INSERT INTO tv_shows (plex_id, title, seasons, episodes, rating, genre, studio, score, year, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        genre = ""
        for e in x.genres:
            genre += e.tag + ','
        args = (x.ratingKey, x.titleSort.encode('utf-8'), len(x.seasons()), len(x.episodes()), str(x.contentRating), genre[:-1], x.studio, x.rating, x.year, x.summary.encode('utf-8'))
        # print(args)
        cur.execute(sql, args)
        # Commit your changes in the database
        print("Inserted: " + x.titleSort)
        db.commit()
    except pymysql.ProgrammingError as e:
        # Rollback in case there is any error
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        FAIL_FLAG = True
        return False
    return True


def update_tv_shows():
    sql = """
    CREATE TABLE IF NOT EXISTS tv_shows
    (
      id              int unsigned NOT NULL auto_increment,
      plex_id         int unsigned NOT NULL,
      title        varchar(255) NOT NULL,
      seasons           int unsigned NOT NULL,
      episodes           int unsigned NOT NULL,
      rating          varchar(255) NOT NULL,
      genre          varchar(255) NOT NULL,
      studio          varchar(255) NOT NULL,
      score           float(8) NOT NULL,
      year            int NOT NULL,
      summary         varchar(1024) NOT NULL,
      PRIMARY KEY     (id)
    );
    """

    try:
        # Execute the SQL command
        cur.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    shows = plex.library.section('TV Shows')
    for show in shows.all():
        if check_in_table(show.ratingKey, 'tv_shows') is not None:
            continue
        else:
            insert_show(show)

    if not FAIL_FLAG:
        db.commit()

    # Use all the SQL you like
    # cur.execute("SELECT * FROM movies")
    # print all the first cell of all the rows
    # for row in cur.fetchall():
    #    print(row)

update_movies()
update_tv_shows()
clean_up()
