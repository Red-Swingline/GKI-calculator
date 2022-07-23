import sqlite3

mydb = sqlite3.connect("gki.db", check_same_thread=False)
db = mydb.cursor()


def create_tables():
    db.execute(
        """CREATE TABLE  IF NOT EXISTS readings(
    id integer PRIMARY KEY,
    r_date TEXT,
    glu REAL,
    key REAL,
    gki REAL
    );"""
    )


