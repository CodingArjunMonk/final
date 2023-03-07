import sqlite3

conn = sqlite3.connect('users.db')
print("Opened database successfully");

conn.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, addr TEXT,'
             'password TEXT)')
print("Table created successfully");
conn.close()