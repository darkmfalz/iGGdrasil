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

def badLogin():
	print 'Content-Type: text/html'
	print

	# print the HTTP body, which is the HTML file representing lecture1.html

	print '''
	<html>
	<head>
		<title>
			Bad Login
		</title>
		<link rel="stylesheet" type="text/css" href="../main.css">
		<link rel="shortcut icon" href="../img/favicon.ico" type="image/x-icon">
		<link rel="icon" href="../img/favicon.ico" type="image/x-icon">
		
		<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
		<script type="text/javascript">
			function loader(){
				window.location.replace("../");
			}
			window.onload = loader
		</script>
	</head>

	<body>
	</body>
	</html>'''

#Checks if there's a cookie already
stored_cookie_string = os.environ.get('HTTP_COOKIE')
#If not, it's a bad login!
if not stored_cookie_string:
	badLogin()
#Otherwise, check the cookie
else:
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	#If the cookie is 'username'
	if 'username' in cookie:
		#If the username submitted in the form is on the cookie
		if(username == cookie['username'].value):
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
						Profile: ''' + username + '''
				</title>
				<link rel="stylesheet" type="text/css" href="../main.css">
				<link rel="shortcut icon" href="../img/favicon.ico" type="image/x-icon">
				<link rel="icon" href="../img/favicon.ico" type="image/x-icon">
				
				<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
				<script>
					function renderImage(file){
						var reader = new FileReader();
						reader.onload = function(event){
							the_url = event.target.result
							$('#some_container_div').html("<img src='" + the_url + "' />")
						}
						reader.readAsDataURL(file);
					}

					$(document).ready(function(){
						document.getElementById('fileinput').addEventListener('change', function(){
							var file = this.files[0];
							// This code is only for demo ...
							console.log("name : " + file.name);
							console.log("size : " + file.size);
							console.log("type : " + file.type);
							console.log("date : " + file.lastModified);
							renderImage(file)
						}, false);
					});
					</script>
				</head>
				
				<body>
					<h1>
						My heading
					</h1>

					<h2>
						''' + username + '''
					</h2>

					<h2>
						Your first name is: ''' + firstname + '''
					</h2>

					<h2>
						Your last name is: ''' + lastname + '''
					</h2>

					<div id="some_container_div">
						<img src= ''' + image + ''' />
					</div>

					<input type="file" id="fileinput" />

					<p>Hello</p>

					<h2>
						My other sub-heading
					</h2>

					<p id="myLine">a new line</p>

					<p>another one</p>
				</body>
			</html>'''
		else:
			badLogin()