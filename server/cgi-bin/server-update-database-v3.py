#!"C:\Python27\python.exe"

import sqlite3

# create a database file named 'people.db' if it doesn't exist yet.
# if this file already exists, then the program will quit.
conn = sqlite3.connect('users.db')
c = conn.cursor()

# create a new 'users' table with three columns: name, age, image
c.execute('create table comments(id varchar(200) primary key not null, username varchar(200), created date, grammar text, parent varchar(200))')
conn.commit()

conn.close()