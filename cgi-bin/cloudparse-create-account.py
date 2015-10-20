#!"C:\Python27\python.exe"

import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage()

requested_username = form['requested_username'].value
requested_firstname = form['requested_firstname'].value
requested_lastname = form['requested_lastname'].value
requested_password = form['requested_password'].value

import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()

import Cookie
import datetime
import os

cookie = Cookie.SimpleCookie()
cookie['username'] = requested_username
expiration = datetime.datetime.now() + datetime.timedelta(days=30)
cookie['username']["expires"] = \
expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

stored_cookie_string = os.environ.get('HTTP_COOKIE')
if not stored_cookie_string:
	pass
else:
	old = Cookie.SimpleCookie(stored_cookie_string)
	if 'username' in old:
		old['username']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

print "Content-type: text/html"

import json
data = {}

data['username'] = requested_username
data['firstname'] = requested_firstname
data['lastname'] = requested_lastname
data['image'] = "../img/v.jpg"

notInDB = True

for r in c.execute('select * from users;'):
	name = r[0]
	if name == requested_username:
		notInDB = False

if notInDB:
	c.execute('insert into accounts values (?, ?, ?, ?, ?)', [requested_username, requested_firstname, requested_lastname, requested_password, "../img/v.jpg"])
	conn.commit()

	print cookie
	print
	print json.dumps(data)

conn.close()