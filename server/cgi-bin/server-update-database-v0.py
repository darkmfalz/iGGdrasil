#!"C:\Python27\python.exe"

import sqlite3

# create a database file named 'people.db' if it doesn't exist yet.
# if this file already exists, then the program will quit.
conn = sqlite3.connect('users.db')
c = conn.cursor()

# create a new 'users' table with three columns: name, age, image
c.execute('create table accounts(username varchar(200) primary key not null, firstname varchar(200) not null, lastname varchar(200) not null, image varchar(200) not null, email varchar(200) not null, password varchar(200) not null, salt varchar(200) not null, created date, loggedin date)')

#Salt 'n' Hash the password
#import hashlib
#import os

#requested_password = "admin"
#rand = os.urandom(64)
#salt = rand.encode('hex')
#requested_password = salt + requested_password
#hash_object = hashlib.sha1(b''+requested_password)
#hex_dig = hash_object.hexdigest()
#requested_password = hex_dig

# insert 1 row of data into the 'accounts' table
#c.execute("insert into accounts values('darkmfalz', 'Adeeb', 'Sheikh', '../img/batman.jpg', 'asheikh4@u.rochester.edu', ?, ?);", [requested_password, salt])

# commit ('save') the transaction and close the connection
#conn.commit()
conn.close()