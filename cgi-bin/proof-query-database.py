#!"C:\Python27\python.exe"

# the above line is for Windows. For Mac OS, use the path to your Python,
# which is usually:
#!/usr/bin/env python


# Lecture 4 - CSC210 Fall 2015
# Philip Guo

# To run:
#
# python lecture4-query-database.py


import sqlite3

# open an existing database file named 'people.db'
conn = sqlite3.connect('users.db')
c = conn.cursor()

# run these SQL queries and print out their results to the terminal:
for r in c.execute('select * from accounts'):
	print r[0] + " " + r[1] + " " + r[2] + " " + r[3] + " " + r[4]
	print
print

wait = input("PRESS ENTER TO TERMINATE.")

conn.close()