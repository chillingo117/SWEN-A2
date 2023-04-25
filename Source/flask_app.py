from flask import Flask
from mysql.connector import connection, Error
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
CONN = connection.MySQLConnection(user='root', password=os.environ['SQL_PASSWORD'], database='VR1Family')
CURSOR = CONN.cursor()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def get_test():
    try:
        retrieveSql = '''
            select * from TestTable;
        '''
        CURSOR.execute(retrieveSql)
        return list(CURSOR)
    except Error as e:
        return e.msg


@app.route("/categories")
def get_categories():
    try:
        retrieveSql = '''
            select * from AidCategories
        '''
        CURSOR.execute(retrieveSql)
        return list(CURSOR)
    except Error as e:
        return e.msg
