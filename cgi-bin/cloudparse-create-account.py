#!"C:\Python27\python.exe"

#CGI Script Imports
import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage()

requested_username = form['requested_username'].value
requested_firstname = form['requested_firstname'].value
requested_lastname = form['requested_lastname'].value
requested_password = form['requested_password'].value

#SQLite Imports
import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()

#Cookie Imports
import Cookie
import datetime
import os

#Creates a new cookie for the current user
cookie = Cookie.SimpleCookie()
cookie['username'] = requested_username
expiration = datetime.datetime.now() + datetime.timedelta(days=30)
cookie['username']["expires"] = \
expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

#Checks if there already is a user cookie in the browser
#If so, the cookie is deleted
stored_cookie_string = os.environ.get('HTTP_COOKIE')
if not stored_cookie_string:
	pass
else:
	old = Cookie.SimpleCookie(stored_cookie_string)
	if 'username' in old:
		old['username']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'

import json
data = {}

data['username'] = requested_username
data['firstname'] = requested_firstname
data['lastname'] = requested_lastname
data['image'] = "../img/v.jpg"

#Salt 'n' Hash the password
import hashlib

rand = os.urandom(64)
salt = rand.encode('hex')
requested_password = salt + requested_password
hash_object = hashlib.sha1(b''+requested_password)
hex_dig = hash_object.hexdigest()
requested_password = hex_dig

#Checks if the current username is already in the database
notInDB = True

for r in c.execute('select * from accounts'):
	name = r[0]
	if name == requested_username:
		notInDB = False

print "Content-type: text/html"

if notInDB:
	c.execute('insert into accounts values (?, ?, ?, ?, ?, ?)', [requested_username, requested_firstname, requested_lastname, "../img/v.jpg",  requested_password, salt])
	conn.commit()

	print cookie
	print
	print json.dumps(data)

conn.close()