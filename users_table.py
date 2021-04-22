import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)'
cur.execute(create_table)

create_user = 'INSERT INTO users VALUES (NULL, ?, ?)'
user = ('anatolii', '123')
cur.execute(create_user, user)

users = [
    ('Elya', '456')
]
cur.executemany(create_user, users)

con.commit()
con.close()