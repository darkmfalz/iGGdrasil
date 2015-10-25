#!"C:\Python27\python.exe"

import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage()

requested_username = form['requested_username'].value
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

for r in c.execute('select * from accounts where username=?', [requested_username]):

	#Salt 'n' Hash the password
	import hashlib

	salt = r[5]
	requested_password = salt + requested_password
	hash_object = hashlib.sha1(b''+requested_password)
	hex_dig = hash_object.hexdigest()
	requested_password = hex_dig

	if(requested_password == r[4]):
		username = r[0]
		firstname = r[1]
		lastname = r[2]
		image = r[3]

		data['username'] = username
		data['firstname'] = firstname
		data['lastname'] = lastname
		data['image'] = image

		print cookie
		print
		print json.dumps(data)

conn.close()