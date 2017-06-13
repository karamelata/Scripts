#!/usr/local/bin/python3
import pymysql
import sys
import urllib.request
import json
import datetime

FAIL_FLAG = False

sqlPswdFile = '/Users/Dave'
SQL_PSWD = open(sqlPswdFile, 'r').readline()[:-1]
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     passwd=SQL_PSWD,
                     db="pihole",
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
      id              			int unsigned NOT NULL auto_increment,
      domains_being_blocked    	int NOT NULL,
      dns_queries_today    		int NOT NULL,
      ads_blocked_today     	int NOT NULL,
      ads_percentage_today     	float(8) NOT NULL,
      unique_domains     		int NOT NULL,
      queries_forwarded     	int NOT NULL,
      queries_cached     		int NOT NULL,
      added           			datetime NOT NULL,
      PRIMARY KEY     			(id)
    );
    """
try:
    cur.execute(sql)
except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

sql = "INSERT INTO stats (domains_being_blocked, dns_queries_today, ads_blocked_today, ads_percentage_today, unique_domains, queries_forwarded, queries_cached, added) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
try:
    with urllib.request.urlopen("http://pi.hole/admin/api.php") as url:
        data = json.loads(url.read().decode())
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = (
        data["domains_being_blocked"],
        data["dns_queries_today"],
        data["ads_blocked_today"],
        data["ads_percentage_today"],
        data["unique_domains"],
        data["queries_forwarded"],
        data["queries_cached"],
        timestamp)
    cur.execute(sql, args)
except pymysql.ProgrammingError as e:
    db.rollback()
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    cleanup(1)
except:
    print("Generic error!")
    cleanup(2)
cleanup()
