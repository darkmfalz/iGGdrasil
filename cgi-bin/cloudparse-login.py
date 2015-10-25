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

import re

EMAIL_REGEX = re.compile(r"[a-zA-z0-9_\-\.]+@[a-zA-z0-9_\-\.]+\.[a-zA-z0-9_\-\.]+")

if EMAIL_REGEX.match(requested_username):

	print "Content-type: text/html"

	import json
	data = {}

	for r in c.execute('select * from accounts where email=?', [requested_username].encode('hex')):

		import Cookie
		import datetime
		import os

		cookie = Cookie.SimpleCookie()
		cookie['username'] = r[0].decode('hex')
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

		#Salt 'n' Hash the password
		import hashlib

		salt = r[6]
		requested_password = salt + requested_password
		hash_object = hashlib.sha1(b''+requested_password)
		hex_dig = hash_object.hexdigest()
		requested_password = hex_dig

		if(requested_password == r[5]):
			username = r[0].decode('hex')
			firstname = r[1].decode('hex')
			lastname = r[2].decode('hex')
			image = r[3].decode('hex')

			data['username'] = username
			data['firstname'] = firstname
			data['lastname'] = lastname
			data['image'] = image

			print cookie
			print
			print json.dumps(data)

	conn.close()
else:

	print "Content-type: text/html"

	import json
	data = {}

	for r in c.execute('select * from accounts where username=?', [requested_username.encode('hex')]):

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

		#Salt 'n' Hash the password
		import hashlib

		salt = r[6]
		requested_password = salt + requested_password
		hash_object = hashlib.sha1(b''+requested_password)
		hex_dig = hash_object.hexdigest()
		requested_password = hex_dig

		if(requested_password == r[5]):
			username = r[0].decode('hex')
			firstname = r[1].decode('hex')
			lastname = r[2].decode('hex')
			image = r[3].decode('hex')

			data['username'] = username
			data['firstname'] = firstname
			data['lastname'] = lastname
			data['image'] = image

			print cookie
			print
			print json.dumps(data)

	conn.close()