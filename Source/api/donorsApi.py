from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from datetime import datetime
from constants import *
import os

donorsApi = Blueprint('donorsApi', __name__,  template_folder='templates')

@donorsApi.route("/donors", methods=['GET'])
def get_donors():
    try:
        sql = f'''
            select id, name from Donors
        '''
        g.CURSOR.execute(sql)
        
        donors=[]
        for id, name in g.CURSOR:
            donors.append({'id': id, 'name': name})

        return donors
    except Error as e:
        return e.msg
    
