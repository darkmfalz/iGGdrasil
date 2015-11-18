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

def noLogin():
	print '''
				<a class="titlelink" class="bannerlink" href="/" title="Go to main page">
				<div style="white-space: nowrap; padding-top: 10px; padding-bottom: 10px;">
					<img src="/img/icons/yggdrasil.png" style="vertical-align:middle" width=100>
					<span>Yggdrasil</span>
				</div>
			</a>

			<div class="logindiv">
				<form action="" id="login">
					<table class="logintable">
						<tr>
							<td>
								Username or Email
							</td>

							<td>
								Password
							</td>
						</tr>

						<tr>
							<td>
								<input type="text" id="username"/>
							</td>

							<td>
								<input type="password" id="password"/>
							</td>

							<td>
								<button id="loginButton">
									Log In
								</button>
							</td>
						</tr>

						<tr>
							<td>
								<div>
									<input type="checkbox" id="persist_box" checked="1"/>
									<label for="persist_box">
										Keep me logged in
									</label>
								</div>
							</td>
							<td>
								<a class="bannerlink"href="/passwordreset">
									Forgot your password?
								</a>
							</td>
						</tr>
					</table>
				</form>
			</div>'''


print 'Content-Type: text/html'
print

#Checks if there's a cookie already
stored_cookie_string = os.environ.get('HTTP_COOKIE')
#If not, it's a prin!
if not stored_cookie_string:
	noLogin()
#Otherwise, check the cookie
else:
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	#If the cookie is 'username'
	if 'username' in cookie:
		cookieUsername = ""
		for r in c.execute('select * from loggedin where sessionid=?', [cookie['username'].value]):
			cookieUsername = r[1].decode('hex')

		username = ""

		for r in c.execute('select * from accounts where username=?', [cookieUsername.encode('hex')]):
			username = r[0].decode('hex')
		#If the username submitted in the form is on the cookie
		if(username == cookieUsername):
			print '''						<a class="titlelink" class="bannerlink" href="/" title="Go to main page">
							<div style="white-space: nowrap; padding-top: 10px; padding-bottom: 10px;">
								<img src="/img/icons/yggdrasil.png" style="vertical-align:middle" width=100>
								<span>Yggdrasil</span>
							</div>
						</a>

						<div class="logindiv">
							<form action="" id="logout">
								<button id="logoutbutton">
									Log Out
								</button>
							</form>
						</div>'''
		else:
			noLogin()
	else:
		noLogin()

conn.close()