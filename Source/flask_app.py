from flask import Flask, g
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

from api.api import api

app = Flask(__name__)
cors = CORS(app, origins=['http://localhost:5173', 'http://scrumtastic-squad:5173', 'http://192.168.1.[0-9]{1,3}:5173'])
app.register_blueprint(api)

@app.before_request
def connect():
    load_dotenv()
    g.CONN = connection.MySQLConnection(user='root', password=os.environ['SQL_PASSWORD'], database='VR1Family')
    g.CURSOR = g.CONN.cursor()

@app.after_request
def disconnect(response):
    g.CONN.commit()
    g.CURSOR.close()
    g.CONN.close()
    return response
