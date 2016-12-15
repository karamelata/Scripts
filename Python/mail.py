import smtplib
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")

parser.parse_args()

FROMADDR = "me@me.com"
LOGIN    = FROMADDR
PASSWORD = "password123"
TOADDRS  = ["example@example.com"]
SUBJECT  = "Hello, World!"

msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
       % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
msg += "It's me, Mail from Python!.\r\n"

server = smtplib.SMTP('smtp.zoho.com', 587)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(LOGIN, PASSWORD)
server.sendmail(FROMADDR, TOADDRS, msg)
server.quit()