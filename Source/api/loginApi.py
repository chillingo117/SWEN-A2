from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import math
import os

loginApi = Blueprint('loginApi', __name__,  template_folder='templates')

@loginApi.route("/login", methods=['POST'])
def login():
    try:
        name = request.json.get('name')
        retrieveSql = f'''
            select * from Passwords where password=%(password)s
        '''
        g.CURSOR.execute(retrieveSql, request.json)
        login = ''
        for (_, profile) in g.CURSOR:
            login = profile
        return login
    except Error as e:
        return e.msg
