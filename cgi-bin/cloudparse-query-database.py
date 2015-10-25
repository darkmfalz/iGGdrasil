#!"C:\Python27\python.exe"

import sqlite3

# open an existing database file named 'people.db'
conn = sqlite3.connect('users.db')
c = conn.cursor()

# run these SQL queries and print out their results to the terminal:
for r in c.execute('select * from accounts'):
	print r[0].decode('hex') + "\n" + r[1].decode('hex') + "\n" + r[2].decode('hex') + "\n" + r[3].decode('hex') + "\n" + r[4].decode('hex') + "\n" + r[5] + "\n" + r[6]
	print

wait = input("PRESS ANY KEY TO TERMINATE.")

conn.close()