from flask import Flask
from mysql.connector import (connection)
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"