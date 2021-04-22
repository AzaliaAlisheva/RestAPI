import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, price real)'
cur.execute(create_table)

create_item = 'INSERT INTO items VALUES (NULL, ?, ?)'
item = ('I want banana too', '123')
cur.execute(create_item, item)

items = [
    ('Potato', '456')
]
cur.executemany(create_item, items)

con.commit()
con.close()