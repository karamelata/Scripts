#!/usr/local/bin/python3
from plexapi.server import PlexServer
from getpass import getpass
import pymysql
import sys
import os
import datetime

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
    sql = "INSERT INTO movies (plex_id, title, director, genre, studio, duration_min, duration_ms, rating, score, year, summary, added, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        genre = ""
        for e in x.genres:
            genre += e.tag + ','
        args = (x.ratingKey, x.titleSort.encode('utf-8'), x.directors[0].tag.encode('utf-8'), genre[:-1], str(
                x.studio), x.duration / 60000, x.duration, str(x.contentRating), x.rating, x.year, x.summary.encode('utf-8'), x.addedAt.strftime('%Y-%m-%d %H:%M:%S'), x.updatedAt.strftime('%Y-%m-%d %H:%M:%S'))
        cur.execute(sql, args)
        # Commit your changes in the database
        print("Inserted MV: %s" % (x.titleSort))
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
      summary         text NOT NULL,
      added             datetime NOT NULL,
      updated           datetime NOT NULL,
      PRIMARY KEY     (id)
    );
    """

    try:
        # Execute the SQL command
        cur.execute(sql)
        # Commit your changes in the database
    except:
        # Rollback in case there is any error
        db.rollback()

    movies = plex.library.section('Movies')
    for x in movies.all():
        if check_in_table(x.ratingKey, 'movies') is not None:
            continue
        else:
            insert_movie(x)

    if FAIL_FLAG:
        sys.exit(1)
    else:
        db.commit()


def insert_show(x):
    sql = "INSERT INTO tv_shows (plex_id, title, seasons, episodes, rating, genre, studio, score, year, summary, added, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        genre = ""
        for e in x.genres:
            genre += e.tag + ','
        args = (x.ratingKey, x.titleSort.encode('utf-8'), len(x.seasons()), len(x.episodes()),
                str(x.contentRating), genre[:-1], x.studio, x.rating, x.year, x.summary.encode('utf-8'), x.addedAt.strftime('%Y-%m-%d %H:%M:%S'), x.updatedAt.strftime('%Y-%m-%d %H:%M:%S'))
        cur.execute(sql, args)
        # Commit your changes in the database
        print("Inserted SH: %s" % (x.titleSort))
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
      summary         text NOT NULL,
      added            datetime NOT NULL,
      updated           datetime NOT NULL,
      PRIMARY KEY     (id)
    );
    """

    try:
        # Execute the SQL command
        cur.execute(sql)
        # Commit your changes in the database
        db.commit()
    except pymysql.ProgrammingError as e:
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0])) 
    shows = plex.library.section('TV Shows')
    for show in shows.all():
        update_tv_episodes(show.episodes())
        if check_in_table(show.ratingKey, 'tv_shows') is not None:
            continue
        else:
            insert_show(show)

    if FAIL_FLAG:
        sys.exit(1)
    else:
        db.commit()


def insert_episode(x):
    sql = "INSERT INTO tv_episodes (plex_id, title, season, ep_index, show_id, duration_min, duration_ms, rating, score, year, summary, added, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        args = (x.ratingKey, x.titleSort.encode('utf-8'), x.parentIndex, x.index,
                x.grandparentRatingKey, x.duration / 60000, x.duration, x.contentRating, x.rating, x.year, x.summary.encode('utf-8'), x.addedAt.strftime('%Y-%m-%d %H:%M:%S'), x.updatedAt.strftime('%Y-%m-%d %H:%M:%S'))
        cur.execute(sql, args)
        # Commit your changes in the database
        print("Inserted EP (%s): %s" % (x.grandparentTitle, x.titleSort))
        #print(datetime.datetime.fromtimestamp(1284286794).strftime('%Y-%m-%d %H:%M:%S'))
    except pymysql.ProgrammingError as e:
        # Rollback in case there is any error
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
        FAIL_FLAG = True
        return False
    db.commit()
    return True


def update_tv_episodes(episodes):
    sql = """
    CREATE TABLE IF NOT EXISTS tv_episodes
    (
      id              int unsigned NOT NULL auto_increment,
      plex_id         int unsigned NOT NULL,
      title        varchar(255) NOT NULL,
      season           int unsigned NOT NULL,
      ep_index           int unsigned NOT NULL,
      show_id           int unsigned NOT NULL,
      duration_min          int unsigned NOT NULL,
      duration_ms           int unsigned NOT NULL,
      rating          varchar(255) NOT NULL,
      score           float(8) DEFAULT 0,
      year            int DEFAULT 0,
      summary         text NOT NULL,
      added             datetime NOT NULL,
      updated             datetime NOT NULL,
      PRIMARY KEY     (id)
    );
    """

    try:
        # Execute the SQL command
        cur.execute(sql)
        # Commit your changes in the database
        db.commit()
    except pymysql.ProgrammingError as e:
        # Rollback in case there is any error
        db.rollback()
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    for ep in episodes:
        if check_in_table(ep.ratingKey, 'tv_episodes') is not None:
            continue
        else:
            insert_episode(ep)
    return

    if FAIL_FLAG:
        sys.exit(1)
    else:
        db.commit()


update_movies()
update_tv_shows()
clean_up()
