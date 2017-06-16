#!/usr/local/bin/python3
import pymysql
import sys
import urllib.request
import json
import subprocess
import datetime

FAIL_FLAG = False

sqlPswdFile = '/home/dave/keys/sql_pswd.txt'
SQL_PSWD = open(sqlPswdFile, 'r').readline()[:-1]
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     passwd=SQL_PSWD,
                     db="network",
                     charset='utf8')
cur = db.cursor()


def cleanup(exit_code=0):
    db.commit()
    cur.close()
    db.close()
    sys.exit(exit_code)

sql = """
    CREATE TABLE IF NOT EXISTS stats
    (
      id                                int unsigned NOT NULL auto_increment,
      ping                              float(10) NOT NULL,
      download                          float(10) NOT NULL,
      upload                            float(10) NOT NULL,
      bytes_sent                        int NOT NULL,
      bytes_received                    int NOT NULL,
      added                             datetime NOT NULL,
      PRIMARY KEY                       (id)
    );
    """
try:
    cur.execute(sql)
except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

sql = "INSERT INTO stats (ping, download, upload, bytes_sent, bytes_received, added) VALUES (%s, %s, %s, %s, %s, %s)"
try:
    output = subprocess.Popen(["speedtest-cli", "--json"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
    data = json.loads(output.decode("utf-8"))
    print(data) 
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = (
        data['ping'],
        data['download'],
        data['upload'],
        data['bytes_sent'],
        data['bytes_received'],
        timestamp)
    cur.execute(sql, args)
except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    cleanup(1)
cleanup()

