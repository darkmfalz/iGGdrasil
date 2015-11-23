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

		for r in c.execute('select * from accounts where username=?', [username.encode('hex')]):
			firstname = r[1].decode('hex')
			lastname = r[2].decode('hex')
			image = r[3].decode('hex')

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

						function shiftProfile(the_url){
							var theImage = new Image();
							theImage.src = the_url;
							var imageHeightRatio = 250/theImage.height;

							if(theImage.width > theImage.height){
								var imageShift = (theImage.width*imageHeightRatio-250)/2;

								console.log(theImage.src);
								console.log(theImage.height);
								console.log(imageShift);

								$("#profilepic").attr("src", the_url);
								$("#profilepic").attr("style", "margin-left: -" + imageShift + "px;");
							}
							if(theImage.width < theImage.height){
								var imageShift = (250-theImage.width*imageHeightRatio)/2;
								$("#profilepic").attr("src", the_url);
								$("#profilepic").attr("style", "margin-left: " + imageShift + "px;");
							}
						}

						shiftProfile($('#profilepic').attr('src'));

						function renderImage(file){
							var reader = new FileReader();
							reader.onload = function(event){
								the_url = event.target.result;
								shiftProfile(the_url);
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
						<div class="profile">
							<h1>
								''' + username + '''
							</h1>

							<h2>
								''' + firstname + ' ' + lastname + '''
							</h2>

							<div class="center-cropped" style='background-image: url("''' + image + '''");'>
								<img id="profilepic" src="''' + image + '''" />
							</div>

						</div>
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
								document.getElementById("editprofile").innerHTML = '<input id="fileinput" type="file" />';

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
						<div class="profile">
							<h1>
								''' + username + '''
							</h1>

							<h2>
								''' + firstname + ' ' + lastname + '''
							</h2>

							<div class="center-cropped" style='background-image: url("''' + image + '''");'>
								<img id="profilepic" src="''' + image + '''" />
							</div>

							<div id="editprofile">
								
							</div>

						</div>
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

conn.close()