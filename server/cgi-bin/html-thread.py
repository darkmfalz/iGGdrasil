#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import datetime
import os

cgitb.enable()

#Retrieve the username and password from the HTML field
form = cgi.FieldStorage()
thread = form['thread'].value

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

firstname = ""
lastname = ""
image = ""

def redirect():
	print 'Content-Type: text/html'
	print

	# print the HTTP body, which is the HTML file representing lecture1.html

	print '''
	<html>
	<head>
		<title>
			Redirecting... | iGG
		</title>
		<link rel="stylesheet" type="text/css" href="../main.css">
		<link rel="shortcut icon" href="../img/icons/favicon.ico" type="image/x-icon">
		<link rel="icon" href="../img/icons/favicon.ico" type="image/x-icon">
		
		<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
		<script type="text/javascript">
			function loader(){
				window.location.replace("../");
			}
			window.onload = loader

		$(document).ready(function(){

			$.ajax({

				url: "/cgi-bin/html-banner.py",

				data: {
				},

				type: "GET",

				dataType: "html",

				success: function(data){

					$("div.banner").html(data);

					$("#username").focus();

				}

			});

		});
		</script>

		<script src="/js-bin/client-login-logout.js" type="text/javascript">
		</script>
	</head>

	<body>
		<div class="wrapper">
			<div class="banner">
			</div>

			<div class="mainpage">
			</div>
		</div>
		
		<div class="footer" xmlns:dc="http://purl.org/dc/elements/1.1/">
			<img src="../img/icons/hr.png" style="vertical-align:middle">
			<p id="copyright" property="dc:rights">&copy;
				<span property="dc:dateCopyrighted">2015</span>
				<span property="dc:publisher">Adeeb Sheikh</span>
			</p>
		</div>

	</body>
	</html>'''

def viewThread():
	proceed = False

	username = ""
	title = ""
	date = ""
	body = ""
	for r in c.execute('select * from grammars'):
		proceed = False
		grammarid = r[0]

		if grammarid == thread:
			proceed = True
			username = r[1].decode('hex')
			date = r[2]
			body = r[3].decode('hex')
			body = body.replace("<", "&lt;")
			body = body.replace(">", "&gt;")
			title = r[4].decode('hex')
			break

	if proceed:
		#Find the user and retrieve the values
		#NOTE: this script doesn't really DO anything if the user doesn't exist and HAS a cookie with a matching username

		firstname = ""
		lastname = ""
		image = ""

		for b in c.execute('select * from accounts where username=?', [username.encode('hex')]):
			firstname = b[1].decode('hex')
			lastname = b[2].decode('hex')
			image = b[3].decode('hex')

		print 'Content-Type: text/html'
		print

		print '''
						<table class="thread">
							<tr>
								<td>
									<div id="parent">
										<table class="post-block">
											<tr>
												<td>
													<a href="/users/''' + username + '''">
														<div class="circle-cropper">
															<img src="''' + image + '''" class="rounded" />
														</div>
													</a>
												</td>

												<td>
													<a href="/threads/''' + thread + '''" style='text-decoration:none;color:black;'>
														<h1>
															''' + title + '''
														</h1>
													</a>
													
													<h2>
														<a href="/users/''' + username + '''" style='text-decoration:none;color:black;'>''' + username + '''</a>
													</h2>
												</td>
											</tr>

											<tr>
												<td>
												</td>

												<td>
													<p style="white-space:pre-wrap;">''' + body + '''</p>
												</td>
											</tr>

											<tr>
												<td>
												</td>

												<td style="opacity: 0.6;">
													''' + date + '''
												</td>
											</tr>
										</table>
									</div>
								</td>
							</tr>'''

		parent = thread

		while proceed:
			proceed = False
			for a in c.execute('select * from comments'):
				proceed = False
			
				if parent == a[4]:
					parent = a[0]
					proceed = True
					username = a[1].decode('hex')
					date = a[2]
					body = a[3].decode('hex')
					body = body.replace("<", "&lt;")
					body = body.replace(">", "&gt;")
					break

			image = "/img/users/v.jpg"

			for a in c.execute('select * from accounts where username=?', [username.encode('hex')]):
				image = a[3].decode('hex')

			if proceed:
				print '''<tr>
							<td>
								<div class="comment">
									<table class="post-block">
										<tr>
											<td>
												<a href="/users/''' + username + '''" style="text-decoration:none;color:black;">
													<div class="circle-cropper">
														<img src="''' + image + '''" class="rounded" />
													</div>
												</a>
											</td>

											<td>
												<a href="/users/''' + username + '''" style="text-decoration:none;color:black;">
													<h2>
														''' + username + '''
													</h2>
												</a>
											</td>

										<tr>
											<td>
											</td>

											<td>
												<p style="white-space:pre-wrap;">''' + body + '''</p>
											</td>
										</tr>
										
										<tr>
											<td>
											</td>

											<td style="opacity: 0.6;">
												''' + date + '''
											</td>
										</tr>
									</table>
								</div>
							</td>
						</tr>'''
				
		print '''
						</table>'''
	else:
		redirect()

#Checks if there's a cookie already
stored_cookie_string = os.environ.get('HTTP_COOKIE')
#If not, it's a bad login!
if not stored_cookie_string:
	viewThread()
#Otherwise, check the cookie
else:
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	#If the cookie is 'username'
	if 'username' in cookie:
		inusername = ""
		for d in c.execute('select * from loggedin where sessionid=?', [cookie['username'].value]):
			inusername = d[1].decode('hex')
		
		inimage = ""
		for r in c.execute('select * from accounts where username=?', [inusername.encode('hex')]):
			inimage = r[3].decode('hex')

		proceed = False

		username = ""
		title = ""
		date = ""
		body = ""
		for r in c.execute('select * from grammars'):
			proceed = False
			grammarid = r[0]

			if grammarid == thread:
				proceed = True
				username = r[1].decode('hex')
				date = r[2]
				body = r[3].decode('hex')
				body = body.replace("<", "&lt;")
				body = body.replace(">", "&gt;")
				title = r[4].decode('hex')
				break

		if proceed:
			#Find the user and retrieve the values
			#NOTE: this script doesn't really DO anything if the user doesn't exist and HAS a cookie with a matching username

			firstname = ""
			lastname = ""
			image = ""

			for b in c.execute('select * from accounts where username=?', [username.encode('hex')]):
				firstname = b[1].decode('hex')
				lastname = b[2].decode('hex')
				image = b[3].decode('hex')

			print 'Content-Type: text/html'
			print

			print '''
							<table class="thread">
								<tr>
									<td>
										<div id="parent">
											<table class="post-block">
												<tr>
													<td>
														<a href="/users/''' + username + '''">
															<div class="circle-cropper">
																<img src="''' + image + '''" class="rounded" />
															</div>
														</a>
													</td>

													<td>
														<a href="/threads/''' + thread + '''" style='text-decoration:none;color:black;'>
															<h1>
																''' + title + '''
															</h1>
														</a>
														
														<h2>
															<a href="/users/''' + username + '''" style='text-decoration:none;color:black;'>''' + username + '''</a>
														</h2>
													</td>
												</tr>

												<tr>
													<td>
													</td>

													<td>
														<p style="white-space:pre-wrap;">''' + body + '''</p>
													</td>
												</tr>

												<tr>
													<td>
													</td>

													<td style="opacity: 0.6;">
														''' + date + '''
													</td>
												</tr>
											</table>
										</div>
									</td>
								</tr>'''

			parent = thread

			while proceed:
				proceed = False
				for a in c.execute('select * from comments'):
					proceed = False
				
					if parent == a[4]:
						parent = a[0]
						proceed = True
						username = a[1].decode('hex')
						date = a[2]
						body = a[3].decode('hex')
						body = body.replace("<", "&lt;")
						body = body.replace(">", "&gt;")
						break

				image = "/img/users/v.jpg"

				for a in c.execute('select * from accounts where username=?', [username.encode('hex')]):
					image = a[3].decode('hex')
				
				if proceed:
					print '''<tr>
								<td>
									<div class="comment">
										<table class="post-block">
											<tr>
												<td>
													<a href="/users/''' + username + '''" style="text-decoration:none;color:black;">
														<div class="circle-cropper">
															<img src="''' + image + '''" class="rounded" />
														</div>
													</a>
												</td>

												<td>
													<a href="/users/''' + username + '''" style="text-decoration:none;color:black;">
														<h2>
															''' + username + '''
														</h2>
													</a>
												</td>

											<tr>
												<td>
												</td>

												<td>
													<p style="white-space:pre-wrap;">''' + body + '''</p>
												</td>
											</tr>
											
											<tr>
												<td>
												</td>

												<td style="opacity: 0.6;">
													''' + date + '''
												</td>
											</tr>
										</table>
									</div>
								</td>
							</tr>'''
			print '''
							<tr>	
								<td>
									<div id="newcomment">
										<form action="" id="createnewcomment" class="input-block">
											<input id="commentparent" type=text size="30" style="display:none; visibility: hidden;" value="''' + parent + '''"/>

											<table>
												<tr>
													<td>
														<a href="/users/''' + inusername + '''">
															<div class="circle-cropper">
																<img src="''' + inimage + '''" class="rounded" />
															</div>
														</a>
													</td>

													<td>
														<ul style="list-style-type: none;">
															<li style="padding-bottom: 5px">
																<h2>Reply</h2>
															</li>

															<li>
																<textarea rows="4" cols="50" id="comment" placeholder="Enter your comment here..."></textarea>
															</li>

															<li>
																<button id="createcommentbutton" style="float:right;">
																	Submit
																</button>
															</li>
														</ul>
													</td>
												</tr>
											</table>
										</form>
									</div>
								</td>
							</tr>
						</table>'''
		else:
			redirect()

	else:
		viewThread()

conn.close()