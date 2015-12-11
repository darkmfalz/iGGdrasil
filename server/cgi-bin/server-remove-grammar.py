#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import datetime
import os
import json

cgitb.enable()

#Retrieve the username and password from the HTML field
form = cgi.FieldStorage()
thread = form['thread'].value

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

data = {}
data['thing'] = "kajigger"

print "Content-type: text/html"
print
print json.dumps(data)

c.execute('delete from comments where root=?', [thread,])
c.execute('delete from grammars where id=?', [thread,])
conn.commit()
conn.close()