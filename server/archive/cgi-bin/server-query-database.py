#!"C:\Python27\python.exe"

import sqlite3

# open an existing database file named 'people.db'
conn = sqlite3.connect('users.db')
c = conn.cursor()

# run these SQL queries and print out their results to the terminal:
while True:
	query = raw_input("Select function: ")
	print
	if(query == "exit"):
		query = input("PRESS ANY KEY TO TERMINATE.")
		conn.close()
	elif(query == "showall"):
		for r in c.execute('select * from accounts'):
			print "Username:\t" + r[0].decode('hex') + "\nFirst Name:\t" + r[1].decode('hex') + "\nLast Name:\t" + r[2].decode('hex') + "\nProfile Image:\t" + r[3].decode('hex') + "\nEmail Address:\t" + r[4].decode('hex') + "\nPassword Hash:\t" + r[5] + "\nPassword Salt:\t" + r[6]
			print
	elif(query == "username"):
		query = raw_input("Select username: ")
		print
		for r in c.execute('select * from accounts where username=?', [query.encode('hex')]):
			print "Username:\t" + r[0].decode('hex') + "\nFirst Name:\t" + r[1].decode('hex') + "\nLast Name:\t" + r[2].decode('hex') + "\nProfile Image:\t" + r[3].decode('hex') + "\nEmail Address:\t" + r[4].decode('hex') + "\nPassword Hash:\t" + r[5] + "\nPassword Salt:\t" + r[6]
			print
	elif(query == "firstname"):
		query = raw_input("Select first name: ")
		print
		for r in c.execute('select * from accounts where firstname=?', [query.encode('hex')]):
			print "Username:\t" + r[0].decode('hex') + "\nFirst Name:\t" + r[1].decode('hex') + "\nLast Name:\t" + r[2].decode('hex') + "\nProfile Image:\t" + r[3].decode('hex') + "\nEmail Address:\t" + r[4].decode('hex') + "\nPassword Hash:\t" + r[5] + "\nPassword Salt:\t" + r[6]
			print
	elif(query == "lastname"):
		query = raw_input("Select last name: ")
		print
		for r in c.execute('select * from accounts where lastname=?', [query.encode('hex')]):
			print "Username:\t" + r[0].decode('hex') + "\nFirst Name:\t" + r[1].decode('hex') + "\nLast Name:\t" + r[2].decode('hex') + "\nProfile Image:\t" + r[3].decode('hex') + "\nEmail Address:\t" + r[4].decode('hex') + "\nPassword Hash:\t" + r[5] + "\nPassword Salt:\t" + r[6]
			print
	elif(query == "email"):
		query = raw_input("Select email address: ")
		print
		for r in c.execute('select * from accounts where email=?', [query.encode('hex')]):
			print "Username:\t" + r[0].decode('hex') + "\nFirst Name:\t" + r[1].decode('hex') + "\nLast Name:\t" + r[2].decode('hex') + "\nProfile Image:\t" + r[3].decode('hex') + "\nEmail Address:\t" + r[4].decode('hex') + "\nPassword Hash:\t" + r[5] + "\nPassword Salt:\t" + r[6]
			print