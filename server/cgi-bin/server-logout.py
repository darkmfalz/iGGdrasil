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
	old = Cookie.SimpleCookie(stored_cookie_string)
	if 'username' in old:
		old['username']['expires']='12-Nov-1995 00:00:00 GMT'
		old['username']['path'] = "/"
		cookie = Cookie.SimpleCookie()
		cookie['username'] = "dil"
		cookie['username']['path'] = "/"
		c.execute('delete from loggedin where sessionid=?', [old['username'].value])
		conn.commit()

		print old
		print
		print json.dumps(data)

conn.close()