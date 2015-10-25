#!"C:\Python27\python.exe"

import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage()

#Retrieve the username and password from the HTML field
requested_username = form['requested_username'].value

#initialize use of the database
import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()


#Comments for this section are just the comments from above
print "Content-type: text/html"

import json
data = {}

#Checks over the accounts for the given username -- the username is encoded in hex, to prevent SQL injection
for r in c.execute('select * from accounts where username=?', [requested_username.encode('hex')]):

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