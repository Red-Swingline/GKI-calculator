import mysql.connector

mydb = mysql.connector.connect(
    host = '10.0.0.3',
    user = 'GKI',
    database = 'GKI',
    passwd = 'password',
    auth_plugin='mysql_native_password'
)

db = mydb.cursor()

def create_table():
    db.execute('CREATE TABLE IF NOT EXISTS user ( \
    user_id INT(8) AUTO_INCREMENT PRIMARY KEY, \
    username VARCHAR(20), \
    bday DATE)')

    db.execute('CREATE TABLE IF NOT EXISTS readings ( \
    id INT(8) AUTO_INCREMENT PRIMARY KEY, \
    user_id INT, \
    ketones FLOAT, \
    glucose FLOAT, \
    rdate DATE)')