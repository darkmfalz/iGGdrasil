#!"C:\Python27\python.exe"

import sqlite3

# create a database file named 'people.db' if it doesn't exist yet.
# if this file already exists, then the program will quit.
conn = sqlite3.connect('users.db')
c = conn.cursor()

# create a new 'users' table with three columns: name, age, image
c.execute('create table accounts(username varchar(100) primary key, firstname varchar(100), lastname varchar(100), password varchar(100), image varchar(100))')

# insert 3 rows of data into the 'users' table
c.execute("insert into accounts values('darkmfalz', 'Adeeb', 'Sheikh', 'admin', '../batman.jpg');")

# commit ('save') the transaction and close the connection
conn.commit()
conn.close()