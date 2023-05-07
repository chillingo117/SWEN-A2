from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from datetime import datetime
from constants import *
import os

acquisitionsApi = Blueprint('acquisitionsApi', __name__,  template_folder='templates')

@acquisitionsApi.route("/acquisition", methods=['POST'])
def make_acquisition():
    try:
        incrementSql = f'''
            update AidItems set amount = amount + %(quantity)s where id = %(selectedId)s
        '''
        g.CURSOR.execute(incrementSql, request.json)
        
        return ''
    except Error as e:
        return e.msg
