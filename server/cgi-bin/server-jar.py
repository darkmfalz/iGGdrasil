#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import datetime
import subprocess
import os
import json

#Retrieve the username and password from the HTML field
form = cgi.FieldStorage()
thread = form['thread'].value

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

grammar = ""
for r in c.execute('select * from grammars'):
	grammarid = r[0]

	if grammarid == thread:
		grammar = r[3].decode('hex')
		break

#Note: can't use '-' or '.' sign
#grammar = '''<S> ::= 'm' <FN> | <FN> ;
#<FN> ::= <DL> | <DL> 'd' <DL> ;
#<DL> ::= <D> | <D> <DL> ;
#<D> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;'''

command = 'java -jar cfgtojson-0.1.1-SNAPSHOT-standalone.jar "' + grammar + '"'

#print command

data = subprocess.check_output(command, shell=True)

print 'Content-Type: application/json'
print
print data

#raw_input("SAY ANYTHING")

conn.close()