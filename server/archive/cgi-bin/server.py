#!"C:\Python27\python.exe"

import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage()

requested_name = form['requested_username'].value

import sqlite3
conn = sqlite3.connect('people.db')
c = conn.cursor()


# print the http header
print "Content-Type: text/html"
print # don't forget the extra newline

import json
data = {}

import Cookie
import os

for r in c.execute('select * from users where name=?;', [requested_username]):
	username = r[0]
	firstname = r[1]
	lastname = r[2]
	image = r[4]

	data['myUsername'] = username
	data['myFirstname'] = firstname
	data['myLastname'] = lastname
	data['myImage'] = image
	print json.dumps(data)

	stored_cookie_string = os.environ.get('HTTP_COOKIE')

	c = Cookie.SimpleCookie()
	c['username'] = username

	if not stored_cookie_string:
		print c
	else:
		old = Cookie.SimpleCookie(stored_cookie_string)
		if 'username' in old:
			old['username']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'
		print c

conn.close()