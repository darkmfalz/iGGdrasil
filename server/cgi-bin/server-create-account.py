#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import datetime
import os
import json
import hashlib
import re

cgitb.enable()

#Retrieve inputs
form = cgi.FieldStorage()
requested_username = form['requested_username'].value
requested_firstname = form['requested_firstname'].value
requested_lastname = form['requested_lastname'].value
requested_password = form['requested_password'].value
requested_email = form['requested_email'].value

#Connect to database
conn = sqlite3.connect('users.db')
c = conn.cursor()

#Creates a new SESSION cookie for the current user
cookie = Cookie.SimpleCookie()
cookie['username'] = requested_username
cookie['username']['path'] = "/"

#Checks if there already is a user cookie in the browser
#If so, the cookie is deleted
stored_cookie_string = os.environ.get('HTTP_COOKIE')
if not stored_cookie_string:
	pass
else:
	old = Cookie.SimpleCookie(stored_cookie_string)
	if 'username' in old:
		old['username']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

data = {}

data['username'] = requested_username
data['firstname'] = requested_firstname
data['lastname'] = requested_lastname
data['image'] = "../img/v.jpg"

#Salt 'n' Hash the password

rand = os.urandom(64)
salt = rand.encode('hex')
requested_password = salt + requested_password
hash_object = hashlib.sha1(b''+requested_password)
hex_dig = hash_object.hexdigest()
requested_password = hex_dig

#Variable telling code to proceed with SQL search or not
proceed = True

#Checks if the given email is even an email address, using REGEX
EMAIL_REGEX = re.compile(r"[a-zA-z0-9_\-\.]+@[a-zA-z0-9_\-\.]+\.[a-zA-z0-9_\-\.]+")
if not EMAIL_REGEX.match(requested_email):
	proceed = False
if EMAIL_REGEX.match(requested_username):
	proceed = False

#Checks if the current username or email is already in the database
for r in c.execute('select * from accounts'):
	name = r[0].decode('hex')
	email = r[4].decode('hex')
	if name == requested_username:
		proceed = False
	if email == requested_email:
		proceed = False

print "Content-type: text/html"

if proceed:
	#inserts the account values into the database, but it encodes them in hex first, to prevent SQL injection
	c.execute('insert into accounts values (?, ?, ?, ?, ?, ?, ?)', [requested_username.encode('hex'), requested_firstname.encode('hex'), requested_lastname.encode('hex'), "../img/v.jpg".encode('hex'), requested_email.encode('hex'), requested_password, salt])
	conn.commit()

	#returns the cookie and json
	print cookie
	print
	print json.dumps(data)

conn.close()