#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import datetime
import os
import json

cgitb.enable()

form = cgi.FieldStorage()

conn = sqlite3.connect('users.db')
c = conn.cursor()

#Comments for this section are just the comments from above
print "Content-type: text/html"

data = {}

stored_cookie_string = os.environ.get('HTTP_COOKIE')
if not stored_cookie_string:
	pass
else:
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	if 'username' in cookie:
		requested_username = ""
		for r in c.execute('select * from loggedin where sessionid=?', [cookie['username'].value]):
			requested_username = r[1]

		#Checks over the accounts for the given username -- the username is encoded in hex, to prevent SQL injection
		for r in c.execute('select * from accounts where username=?', [requested_username]):

			username = r[0].decode('hex')
			firstname = r[1].decode('hex')
			lastname = r[2].decode('hex')
			image = r[3].decode('hex')

			data['username'] = username
			data['firstname'] = firstname
			data['lastname'] = lastname
			data['image'] = image

			print
			print json.dumps(data)

conn.close()