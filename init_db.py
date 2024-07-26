import sqlite3

con = sqlite3.connect('auth.db')

with open('schema.sql') as f:
    con.executescript(f.read())

con.commit()
con.close()