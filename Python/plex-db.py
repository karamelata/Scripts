#!/usr/local/bin/python3
from plexapi.server import PlexServer
from getpass import getpass
import pymysql
import sys
import os
import datetime

FAIL_FLAG = False

pswd = getpass("MySQL Password:")
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     passwd=pswd,
                     db="plex",
                     charset='utf8')

cur = db.cursor()
plex = PlexServer('http://127.0.0.1:1234', os.environ['PLEX_TOKEN'])


def clean_up():
  db.commit()
  cur.close()
  db.close()
  sys.exit(0)


def check_in_table(id_to_check, table_name):
  sql = "SELECT * FROM %s WHERE `plex_id`=%s" % (
      table_name, str(id_to_check))
  cur.execute(sql)
  return cur.fetchone()


def update_timestamp(id, media_type):
  sql = """
    CREATE TABLE IF NOT EXISTS update_log
    (
      id              int unsigned NOT NULL auto_increment,
      plex_id         int unsigned NOT NULL,
      type            varchar(16) NOT NULL,
      added           datetime NOT NULL,
      updated         datetime NOT NULL,
      PRIMARY KEY     (id)
    );
    """
  try:
    cur.execute(sql)
  except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    return
  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  result = check_in_table(id, "update_log")
  if result is None:
    sql = "INSERT INTO update_log (plex_id, type, added, updated) VALUES (%s, %s, %s, %s)"
    args = (id, media_type, now, now)
    cur.execute(sql, args)
  else:
    sql = "UPDATE update_log SET updated = %s WHERE `plex_id` = %s"
    args = (now, id)
    cur.execute(sql, args)


def insert_movie(x):
  sql = "INSERT INTO movies (plex_id, title, title_sort, director, genre, studio, duration_min, duration_ms, rating, score, year, summary, added, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  try:
    genre = ""
    for e in x.genres:
      genre += e.tag + ','
    if x.studio is None:
      x.studio = "NULL"
    args = (x.ratingKey, x.title, x.titleSort, x.directors[0].tag, genre[:-1], str(
            x.studio), x.duration / 60000, x.duration, str(x.contentRating), x.rating, x.year, x.summary, x.addedAt.strftime('%Y-%m-%d %H:%M:%S'), x.updatedAt.strftime('%Y-%m-%d %H:%M:%S'))
    cur.execute(sql, args)
    update_timestamp(x.ratingKey, "movie")
    print("Inserted MV: %s" % (x.title))
  except pymysql.ProgrammingError as e:
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
      title_sort      varchar(255) NOT NULL,
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
    cur.execute(sql)
  except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

  movies = plex.library.section('Movies')
  for x in movies.all():
    if check_in_table(x.ratingKey, 'movies') is not None:
      continue
    else:
      insert_movie(x)

  if FAIL_FLAG:
    sys.exit(1)


def insert_show(x):
  sql = "INSERT INTO tv_shows (plex_id, title, title_sort, seasons, episodes, rating, studio, score, year, summary, added, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  try:
    args = (x.ratingKey, x.title, x.titleSort, len(x.seasons()), len(x.episodes()),
            str(x.contentRating), x.studio, x.rating, x.year, x.summary, x.addedAt.strftime('%Y-%m-%d %H:%M:%S'), x.updatedAt.strftime('%Y-%m-%d %H:%M:%S'))
    cur.execute(sql, args)
    update_timestamp(x.ratingKey, "tv_show")
    print("Inserted SH: %s" % (x.title))
  except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    return False
  return True


def update_tv_shows():
  sql = """
    CREATE TABLE IF NOT EXISTS tv_shows
    (
      id              int unsigned NOT NULL auto_increment,
      plex_id         int unsigned NOT NULL,
      title        varchar(255) NOT NULL,
      title_sort        varchar(255) NOT NULL,
      seasons           int unsigned NOT NULL,
      episodes           int unsigned NOT NULL,
      rating          varchar(255) NOT NULL,
      # genre          varchar(255) NOT NULL,
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
    cur.execute(sql)
  except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
  shows = plex.library.section('TV Shows')
  for show in shows.all():
    if check_in_table(show.ratingKey, 'tv_shows') is None:
      insert_show(show)
    update_tv_episodes(show.episodes())

  if FAIL_FLAG:
    sys.exit(1)


def insert_episode(x):
  global FAIL_FLAG
  sql = "INSERT INTO tv_episodes (plex_id, title, title_sort, season, ep_index, show_id, duration_min, duration_ms, rating, score, year, summary, added, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  try:
    args = (x.ratingKey, x.title, x.titleSort, x.parentIndex, x.index,
            x.grandparentRatingKey, x.duration / 60000, x.duration, x.contentRating, x.rating, x.year, x.summary, x.addedAt.strftime('%Y-%m-%d %H:%M:%S'), x.updatedAt.strftime('%Y-%m-%d %H:%M:%S'))
    cur.execute(sql, args)
    update_timestamp(x.ratingKey, "tv_episode")
    print("Inserted EP (%s): S%sE%s: %s" %
          (x.grandparentTitle, x.parentIndex, x.index, x.title))
    # print(datetime.datetime.fromtimestamp(1284286794).strftime('%Y-%m-%d
    # %H:%M:%S'))
  except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    FAIL_FLAG = True
    return False
  # Skip any rogue entries (specials, pilots, etc)
  except AttributeError as e:
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    print("Skipping: (%s): %s" % (x.grandparentTitle, x.title))
    return False
  return True


def update_tv_episodes(episodes):
  sql = """
    CREATE TABLE IF NOT EXISTS tv_episodes
    (
      id              int unsigned NOT NULL auto_increment,
      plex_id         int unsigned NOT NULL,
      title        varchar(255) NOT NULL,
      title_sort        varchar(255) NOT NULL,
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
    cur.execute(sql)
  except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

  for ep in episodes:
    if check_in_table(ep.ratingKey, 'tv_episodes') is not None:
      continue
    else:
      insert_episode(ep)
  if FAIL_FLAG:
    sys.exit(1)


def checkup_movies():
  movies = plex.library.section('Movies').all()
  try:
    cur.execute("SELECT * FROM movies")
  except pymysql.ProgrammingError as e:
    if e.args[0] == 1146:
      print("Movies table doesn't exist- skipping checkup")
      return
  for row in cur.fetchall():
    success = False
    for movie in movies:
      if int(row[1]) == int(movie.ratingKey) and int(row[8]) == int(movie.duration):
        success = True
        break
    if not success:
      cur.execute("DELETE FROM movies WHERE plex_id=%s" % row[1])
      print("Removed: %s" % row[2])


checkup_movies()
update_movies()
update_tv_shows()
clean_up()
