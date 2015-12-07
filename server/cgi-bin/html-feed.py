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

conn2 = sqlite3.connect('users.db')
c2 = conn.cursor()

def printThread(r):
	image = ""

	for a in c2.execute('select * from accounts where username=?', [r[1]]):
		image = a[3].decode('hex')

	body = r[3].decode('hex')
	body = body.replace("<", "&lt;")
	body = body.replace(">", "&gt;")

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

print 'Content-Type: text/html'
print

print "<table class='threadnm'>"

for r in c.execute('select * from grammars order by created desc'):
	print "<tr><td>"
	printThread(r)
	print "</td></tr>"

print "</table>"

conn.close()
conn2.close()