#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import datetime
import os

cgitb.enable()

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

def printThread(r):
	print '''
<h1>''' + r[4].decode('hex') + '''</h1>
<h2>Published on ''' + r[2] + ''' by ''' + r[1].decode('hex') + '''</h2>
<h2>Body:</h2>
<p>''' + r[3].decode('hex') + '''</p>'''


print 'Content-Type: text/html'
print

print "<table>"
for r in c.execute('select * from grammars order by created desc'):
	print "<tr><td style='white-space:pre-wrap;'>"
	printThread(r)
	print "</td></tr>"
print "</table>"

conn.close()