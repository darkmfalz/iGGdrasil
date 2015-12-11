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

conn2 = sqlite3.connect('users.db')
c2 = conn2.cursor()

data = {}
data['thing'] = "kajigger"

print "Content-type: text/html"
print
print json.dumps(data)

for r in c.execute('select * from comments where id=?', [thread,]):
	c2.execute('update comments set parent=? where parent=?', [r[4], thread])

c.execute('delete from comments where id=?', [thread,])
conn.commit()
conn2.commit()
conn.close()
conn2.close()