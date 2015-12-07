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
username = form['username'].value

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

conn2 = sqlite3.connect('users.db')
c2 = conn.cursor()

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

def viewProfile():
	proceed = False

	for r in c.execute('select * from accounts'):
		name = r[0].decode('hex')
		if name == username:
			proceed = True

	if proceed:
		#Find the user and retrieve the values
		#NOTE: this script doesn't really DO anything if the user doesn't exist and HAS a cookie with a matching username
		firstname = ""
		lastname = ""
		image = ""
		email = ""

		for r in c.execute('select * from accounts where username=?', [username.encode('hex')]):
			firstname = r[1].decode('hex')
			lastname = r[2].decode('hex')
			image = r[3].decode('hex')
			email = r[4].decode('hex')

		# prints a minimal HTTP header
		print 'Content-Type: text/html'
		print

		print '''
			<html>
			<head>
				<title>
						''' + username + ''' | iGG
				</title>
				<link rel="stylesheet" type="text/css" href="../main.css">
				<link rel="shortcut icon" href="../img/icons/favicon.ico" type="image/x-icon">
				<link rel="icon" href="../img/icons/favicon.ico" type="image/x-icon">
				
				<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
				<script>
					$(document).ready(function(){
						
						function renderImage(file){
							var reader = new FileReader();
							reader.onload = function(event){
								the_url = event.target.result;
								$("#profilepic").attr("src", the_url);
								var str1 = "url(";
								var str2 = str1.concat(the_url);
								var str3 = ")";
								var str4 = str2.concat(str3);
								$(".center-cropped").css("background-image", str4);
							}
							reader.readAsDataURL(file);
						}

						$.ajax({

							url: "/cgi-bin/html-banner.py",

							data: {
							},

							type: "GET",

							dataType: "html",

							success: function(data){

								$("div.banner").html(data);

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
						<table class="profile">
							<tr>
								<td>
									<table class="profile-block" id="infopanel">
										<tr>
											<td>
												<h1>
													''' + username + '''
												</h1>
											</td>
										</tr>

										<tr>
											<td>
												<h2>
													''' + firstname + ' ' + lastname + '''
												</h2>
											</td>
										</tr>

										<tr>
											<td>
												<div class="center-cropped" style='background-image: url("''' + image + '''");'>
													<img id="profilepic" src="''' + image + '''" />
												</div>
											</td>
										</tr>
									</table>
								</td>

								<td>
									<table class="profile-block">'''

		gnexist = True

		for r in c.execute('select * from grammars where username=? order by created desc', [username.encode('hex')]):
			gnexist = False
			body = r[3].decode('hex')
			body = body.replace("<", "&lt;")
			body = body.replace(">", "&gt;")
			print "<tr><td>"
			print '''
			<table class="post-block">
				<tr>
					<td>
						<a href="/users/''' + r[1].decode('hex') + '''">
							<div class="circle-cropper">
								<img src="''' + image + '''" class="rounded" />
							</div>
						</a>
					</td>

					<td>
						<a href="/threads/''' + r[0] + '''" style='text-decoration:none;color:black;'>
							<h1>
								''' + r[4].decode('hex') + '''
							</h1>
						</a>
						
						<h2>
							<a href="/users/''' + r[1].decode('hex') + '''" style='text-decoration:none;color:black;'>''' + r[1].decode('hex') + '''</a>
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
						''' + r[2] + '''
					</td>
				</tr>
			</table>'''
			print "</td></tr>"

		if(gnexist):
			print "<tr><td><h3>No grammars to show!</h3></td></tr>"
		print '''	</table>
		</td>

		<td>
			<table class="profile-block">'''

		cnexist = True

		for r in c.execute('select * from comments where username=? order by created desc', [username.encode('hex')]):
			cnexist = False

			threadtitle = ""
			for a in c2.execute('select * from grammars where id=?', [r[5]]):
				threadtitle = a[4].decode('hex')

			body = r[3].decode('hex')
			body = body.replace("<", "&lt;")
			body = body.replace(">", "&gt;")

			print '<tr><td>'
			print '''
			<table class="post-block">
				<tr>
					<td>
						<a href="/threads/''' + r[5] + '''" style='text-decoration:none;color:black;'>
							<h3>
								''' + threadtitle + '''
							</h3>
						</a>
					</td>
				</tr>

				<tr>
					<td>
						<p style="white-space:pre-wrap;">''' + body + '''</p>
					</td>
				</tr>

				<tr>
					<td style="opacity: 0.6;">
						''' + r[2] + '''
					</td>
				</tr>
			</table>'''
			print "</td></tr><tr>"

		if(cnexist):
			print "<tr><td><h3>No comments to show!</h3></td></tr>"

		print '''						</table>
							</td>
						</tr>
					</table>
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
	else:
		redirect()

#Checks if there's a cookie already
stored_cookie_string = os.environ.get('HTTP_COOKIE')
#If not, it's a bad login!
if not stored_cookie_string:
	viewProfile()
#Otherwise, check the cookie
else:
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	#If the cookie is 'username'
	if 'username' in cookie:
		cookieUsername = ""
		for r in c.execute('select * from loggedin where sessionid=?', [cookie['username'].value]):
			cookieUsername = r[1].decode('hex')
		#If the username submitted in the form is on the cookie
		if(username == cookieUsername):
			#Then, find the user and retrieve the values
			#NOTE: this script doesn't really DO anything if the user doesn't exist and HAS a cookie with a matching username
			for r in c.execute('select * from accounts where username=?', [username.encode('hex')]):
				firstname = r[1].decode('hex')
				lastname = r[2].decode('hex')
				image = r[3].decode('hex')
				email = r[4].decode('hex')

			# prints a minimal HTTP header
			print 'Content-Type: text/html'
			print

			# print the HTTP body, which is the HTML file representing lecture1.html

			print '''
			<html>
			<head>
				<title>
						''' + username + ''' | iGG
				</title>
				<link rel="stylesheet" type="text/css" href="../main.css">
				<link rel="shortcut icon" href="../img/icons/favicon.ico" type="image/x-icon">
				<link rel="icon" href="../img/icons/favicon.ico" type="image/x-icon">
				
				<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
				<script>

					$(document).ready(function(){

						$.ajax({

							url: "/cgi-bin/server-authenticate.py",

							data: {
							},

							type: "GET",

							dataType: "json",

							success: function(data){

								console.log("Currently logged in as:");
								console.log(data.username);
								document.getElementById("editprofile").innerHTML = '<ul style="list-style-type:none"><li>Change Profile Picture</li><li><input id="fileinput" type="file" /></li></ul>';

								document.getElementById('fileinput').addEventListener('change', function(){
									var file = this.files[0];
									console.log("name : " + file.name);
									console.log("size : " + file.size);
									console.log("type : " + file.type);
									console.log("date : " + file.lastModified);
									renderImage(file)

									var reader1 = new FileReader();
									reader1.onload = function(event){
										the_url = event.target.result;
										console.log(the_url);

										$.ajax({

											url: "/cgi-bin/server-change-picture.py",

											data: {
												url: the_url
											},

											type: "POST",

											dataType: "html",

											success: function(){

											}

										});

									}
									reader1.readAsDataURL(file);
									
								}, false);

							},

							error: function(){

								console.log("Not logged in.");

							}

						});

						function renderImage(file){
							var reader = new FileReader();
							reader.onload = function(event){
								the_url = event.target.result;
								$("#profilepic").attr("src", the_url);
								var str1 = "url(";
								var str2 = str1.concat(the_url);
								var str3 = ")";
								var str4 = str2.concat(str3);
								$(".center-cropped").css("background-image", str4);
							}
							reader.readAsDataURL(file);
						}

						$.ajax({

							url: "/cgi-bin/html-banner.py",

							data: {
							},

							type: "GET",

							dataType: "html",

							success: function(data){

								$("div.banner").html(data);

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
						<table class="profile">
							<tr>
								<td>
									<table class="profile-block" id="infopanel">
										<tr>
											<td>
												<h1>
													''' + username + '''
												</h1>
											</td>
										</tr>

										<tr>
											<td>
												<h2>
													''' + firstname + ' ' + lastname + '''
												</h2>
											</td>
										</tr>

										<tr>
											<td>
												<div class="center-cropped" style='background-image: url("''' + image + '''");'>
													<img id="profilepic" src="''' + image + '''" />
												</div>
											</td>
										</tr>

										<tr>
											<td>
												<div id="editprofile">
													
												</div>
											</td>
										</tr>
									</table>
								</td>

								<td>
									<table class="profile-block">'''

			gnexist = True

			for r in c.execute('select * from grammars where username=? order by created desc', [username.encode('hex')]):
				gnexist = False
				body = r[3].decode('hex')
				body = body.replace("<", "&lt;")
				body = body.replace(">", "&gt;")
				print "<tr><td>"
				print '''
				<table class="post-block">
					<tr>
						<td>
							<a href="/users/''' + r[1].decode('hex') + '''">
								<div class="circle-cropper">
									<img src="''' + image + '''" class="rounded" />
								</div>
							</a>
						</td>

						<td>
							<a href="/threads/''' + r[0] + '''" style='text-decoration:none;color:black;'>
								<h1>
									''' + r[4].decode('hex') + '''
								</h1>
							</a>
							
							<h2>
								<a href="/users/''' + r[1].decode('hex') + '''" style='text-decoration:none;color:black;'>''' + r[1].decode('hex') + '''</a>
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
							''' + r[2] + '''
						</td>
					</tr>
				</table>'''
				print "</td></tr>"

			if(gnexist):
				print "<tr><td><h3>No grammars to show!</h3></td></tr>"
			print '''	</table>
			</td>

			<td>
				<table class="profile-block">'''

			cnexist = True

			for r in c.execute('select * from comments where username=? order by created desc', [username.encode('hex')]):
				cnexist = False

				threadtitle = ""
				for a in c2.execute('select * from grammars where id=?', [r[5]]):
					threadtitle = a[4].decode('hex')

				body = r[3].decode('hex')
				body = body.replace("<", "&lt;")
				body = body.replace(">", "&gt;")

				print '<tr><td>'
				print '''
				<table class="post-block">
					<tr>
						<td>
							<a href="/threads/''' + r[5] + '''" style='text-decoration:none;color:black;'>
								<h3>
									''' + threadtitle + '''
								</h3>
							</a>
						</td>
					</tr>

					<tr>
						<td>
							<p style="white-space:pre-wrap;">''' + body + '''</p>
						</td>
					</tr>

					<tr>
						<td style="opacity: 0.6;">
							''' + r[2] + '''
						</td>
					</tr>
				</table>'''
				print "</td></tr><tr>"

			if(cnexist):
				print "<tr><td><h3>No comments to show!</h3></td></tr>"

			print '''						</table>
								</td>
							</tr>
						</table>
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
		else:
			viewProfile()
	else:
		viewProfile()

conn.close()