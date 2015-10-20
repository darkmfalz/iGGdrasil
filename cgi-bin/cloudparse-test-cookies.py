#!"C:\Python27\python.exe"

import cgitb
cgitb.enable()

import datetime

import cgi
form = cgi.FieldStorage()

import Cookie
import os

dname = form['my_name'].value

stored_cookie_string = os.environ.get('HTTP_COOKIE')
if not stored_cookie_string:
	print 'error'
else:
	cook = Cookie.SimpleCookie(stored_cookie_string)

	if 'username' in cook:
		my_name = cook['username'].value

	print 'Content-Type: text/html'
	print

	print '<html>'
	print '	<head>'

	print '		<title>'
	print '''
				My first webpage
			</title>
			<link rel="stylesheet" type="text/css" href="../proof.css">
		</head>
	'''

	print '<body>'
	print '		<h1>My heading</h1>'

	import sqlite3

	conn = sqlite3.connect('users.db')
	c = conn.cursor()

	for r in c.execute('select * from accounts;'):
		name = r[0]
		print '<h1>' + name + '</h1>'
		print '<hr/>'
	conn.close()

	print '		<h2>'
	print str(datetime.datetime.now())
	#print '			My sub-heading'
	print '		</h2>'

	print '<h2>Your name is: ' + my_name + dname +'</h2>'

	print '''
			<p>Hello ''' + my_name + '''</p>
			<h2>
				My other sub-heading
			</h2>

			<p id="myLine">a new line</p>
			<p>another one</p>'''

	print'''	</body>
	</html>'''