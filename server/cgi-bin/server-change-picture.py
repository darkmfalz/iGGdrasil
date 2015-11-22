#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import os
import datetime
import urllib

cgitb.enable()

#Retrieve the username and password from the HTML field
form = cgi.FieldStorage()
url = form['url'].value

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

stored_cookie_string = os.environ.get('HTTP_COOKIE')
#If not, it's a bad login!
if not stored_cookie_string:
	pass
#Otherwise, check the cookie
else:
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	#If the cookie is 'username'
	if 'username' in cookie:
		cookieUsername = ""
		for r in c.execute('select * from loggedin where sessionid=?', [cookie['username'].value]):
			username = r[1].decode('hex')
		#Then, find the user and retrieve the values
		#NOTE: this script doesn't really DO anything if the user doesn't exist and HAS a cookie with a matching username
		for r in c.execute('select * from accounts where username=?', [username.encode('hex')]):
			now = datetime.datetime.now()
			nowString = now.strftime("%a, %d-%b-%Y %H:%M:%S EST")
			pid = nowString + username
			pid = pid.encode('hex')
			urllib.urlretrieve(url, "../img/users/" + pid + ".jpg")
			img = "/img/users/" + pid + ".jpg"
			c.execute("update accounts set image=? where username=?", [img.encode('hex'), username.encode('hex')])
			conn.commit()
			print 'Content-Type: text/html'
			print