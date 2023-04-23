from flask import Flask
from mysql.connector import (connection)
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def get_test():
    load_dotenv()
    password = os.environ['SQL_PASSWORD']
    try:
        conn = connection.MySQLConnection(user='root', password=password, database='VR1Family')
        cursor = conn.cursor()
        retrieveSql = '''
            select * from TestTable;
        '''
        cursor.execute(retrieveSql)
        return list(cursor)
    except:
        return 'error in query'