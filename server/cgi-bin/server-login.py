#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import re
import json
import Cookie
import datetime
import os
import hashlib

#For error testing if the cgi scripts end up all wonky.
#But it's surprisingly unhelpful for cgi scripts that don't load pages.
cgitb.enable()

#Retrieve the username and password from the HTML field
form = cgi.FieldStorage()
requested_username = form['requested_username'].value
requested_password = form['requested_password'].value
keep_loggedin = form['keep_loggedin'].value

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

#Tests the input to see if it's an email -- using REGEX
EMAIL_REGEX = re.compile(r"[a-zA-z0-9_\-\.]+@[a-zA-z0-9_\-\.]+\.[a-zA-z0-9_\-\.]+")

#If it's an email according to REGEX...
if EMAIL_REGEX.match(requested_username):

	#print HTML heading
	print "Content-type: text/html"

	data = {}

	#Checks over the accounts for the given email -- the email is encoded in hex, to prevent SQL injection
	for r in c.execute('select * from accounts where email=?', [requested_username.encode('hex')]):
		rand = os.urandom(64)
		sessionid = rand.encode('hex')
		#Create a new cookie from the username
		cookie = Cookie.SimpleCookie()
		#The username in the cookie is the DECODED hex retrieved from the database
		cookie['username'] = sessionid
		expiration = datetime.datetime.now() + datetime.timedelta(days=36500)
		#If the user has specified that this is NOT a session cookie, set expiration:
		if(keep_loggedin == "TRUE"):
			cookie['username']["expires"] = \
			expiration.strftime("%a, %d-%b-%Y %H:%M:%S EST")
		cookie['username']['path'] = "/"

		#If a cookie already exists, destroy it!
		stored_cookie_string = os.environ.get('HTTP_COOKIE')
		if not stored_cookie_string:
			pass
		else:
			old = Cookie.SimpleCookie(stored_cookie_string)
			if 'username' in old:
				old['username']['expires']='Sun, 12 Nov 1995 00:00:00 GMT'
				c.execute('delete from loggedin where sessionid=?', [old['username'].value])
				conn.commit()

		#Salt 'n' Hash the password using the stored salt to test it against the password in the database
		salt = r[6]
		#appends the salt to start of the password
		requested_password = salt + requested_password
		#hashes the password and salt using SHA1
		hash_object = hashlib.sha1(b''+requested_password)
		#Retrieves the hash as a hex digest
		hex_dig = hash_object.hexdigest()
		requested_password = hex_dig

		if(requested_password == r[5]):
			#pass the account fields to the JSON after they've been decoded from hex
			username = r[0].decode('hex')
			firstname = r[1].decode('hex')
			lastname = r[2].decode('hex')
			image = r[3].decode('hex')

			data['username'] = username
			data['firstname'] = firstname
			data['lastname'] = lastname
			data['image'] = image

			c.execute('insert into loggedin values (?, ?)', [sessionid, requested_username.encode('hex')])
			conn.commit()

			#Return the cookie and JSON
			print cookie
			print
			print json.dumps(data)
else:

	#print HTML heading
	print "Content-type: text/html"

	data = {}

	#Checks over the accounts for the given username -- the username is encoded in hex, to prevent SQL injection
	for r in c.execute('select * from accounts where username=?', [requested_username.encode('hex')]):
		rand = os.urandom(64)
		sessionid = rand.encode('hex')
		#Create a new cookie from the username
		cookie = Cookie.SimpleCookie()
		#The username in the cookie is the DECODED hex retrieved from the database
		cookie['username'] = sessionid
		expiration = datetime.datetime.now() + datetime.timedelta(days=36500)
		#If the user has specified that this is NOT a session cookie, set expiration:
		if(keep_loggedin == "TRUE"):
			cookie['username']["expires"] = \
			expiration.strftime("%a, %d-%b-%Y %H:%M:%S EST")
		cookie['username']['path'] = "/"

		#If a cookie already exists, destroy it!
		stored_cookie_string = os.environ.get('HTTP_COOKIE')
		if not stored_cookie_string:
			pass
		else:
			old = Cookie.SimpleCookie(stored_cookie_string)
			if 'username' in old:
				old['username']['expires']='Sun, 12 Nov 1995 00:00:00 GMT'
				c.execute('delete from loggedin where sessionid=?', [old['username'].value])
				conn.commit()

		#Salt 'n' Hash the password using the stored salt to test it against the password in the database
		salt = r[6]
		#appends the salt to start of the password
		requested_password = salt + requested_password
		#hashes the password and salt using SHA1
		hash_object = hashlib.sha1(b''+requested_password)
		#Retrieves the hash as a hex digest
		hex_dig = hash_object.hexdigest()
		requested_password = hex_dig

		if(requested_password == r[5]):
			#pass the account fields to the JSON after they've been decoded from hex
			username = r[0].decode('hex')
			firstname = r[1].decode('hex')
			lastname = r[2].decode('hex')
			image = r[3].decode('hex')

			data['username'] = username
			data['firstname'] = firstname
			data['lastname'] = lastname
			data['image'] = image

			c.execute('insert into loggedin values (?, ?)', [sessionid, requested_username.encode('hex')])
			conn.commit()

			#Return the cookie and JSON
			print cookie
			print
			print json.dumps(data)
conn.close()