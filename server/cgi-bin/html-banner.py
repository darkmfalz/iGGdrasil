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
					<img src="/img/icons/igg.png" style="vertical-align:middle" width=100>
					<img src="/img/icons/whitetitle.png" style="vertical-align:middle">
				</div>
			</a>

			<div class="logindiv">
				<form action="" id="login">
					<table class="logintable">
						<tr>
							<td style="color: rgb(255, 255, 255);">
								Username or Email
							</td>

							<td style="color: rgb(255, 255, 255);">
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
							<td style="color: rgb(255, 255, 255);">
								<div>
									<input type="checkbox" id="persist_box" checked="1"/>
									<label for="persist_box">
										Keep me logged in
									</label>
								</div>
							</td>
							<td style="color: rgb(255, 255, 255);">
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
		image = ""

		for r in c.execute('select * from accounts where username=?', [cookieUsername.encode('hex')]):
			username = r[0].decode('hex')
			image = r[3].decode('hex')
		#If the username submitted in the form is on the cookie
		if(username == cookieUsername):
			print '''
						<a class="titlelink" class="bannerlink" href="/" title="Go to main page">
							<div style="white-space: nowrap; padding-top: 10px; padding-bottom: 10px;">
								<img src="/img/icons/igg_notext.png" style="vertical-align:middle" width=50>
							</div>
						</a>

						<div class="logoutdiv">
							<table class="logintable">
								<tr>

									<td>
										<a href="/users/''' + username + '''">
											<div class="banner-button">
												<img src="/img/icons/email-4096-black.png" />
											</div>
										</a>
									</td>

									<td>
										<a href="/users/''' + username + '''">
											<div class="banner-button">
												<img src="/img/icons/gear.png" />
											</div>
										</a>
									</td>

									<td>
										<a href="/users/''' + username +'''">
											<div class="circle-cropper">
												<img src="''' + image + '''" class="rounded" />
											</div>
										</a>
									</td>

									<td>
										<form action="" id="logout">
											<button id="logoutbutton">
												Log Out
											</button>
										</form>
									</td>
								</tr>
							</table>
						</div>'''
		else:
			noLogin()
	else:
		noLogin()

conn.close()