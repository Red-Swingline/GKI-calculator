import sqlite3

mydb = sqlite3.connect("gki.db", check_same_thread=False)
db = mydb.cursor()


def create_tables():
    db.execute(
        """CREATE TABLE  IF NOT EXISTS readings(
    id integer PRIMARY KEY,
    glu REAL,
    key REAL,
    gki REAL
    );"""
    )

    db.execute(
        """CREATE TABLE  IF NOT EXISTS frun(
    id integer PRIMARY KEY,
    first_run BOOLEAN
    );"""
    )

    db.execute(
        """CREATE TABLE IF NOT EXISTS user_info(
        id integer PRIMARY KEY,
        age integer,
        height TEXT,
        weight REAL,
        metric BOOLEAN
    );"""
    )
