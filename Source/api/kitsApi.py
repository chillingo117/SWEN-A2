from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

kitsApi = Blueprint('kitsApi', __name__,  template_folder='templates')


@kitsApi.route("/kits", methods=['GET'])
def get_kits():
    kits = []
    try:
        retrieveSql = '''
            select * from `Kits`
        '''
        g.CURSOR.execute(retrieveSql)

        for (id, name) in g.CURSOR:
            kits.append({'id': id, 'name': name})
        return kits
    except Error as e:
        return e.msg

@kitsApi.route("/kits/create", methods=['POST'])
def create_category():
    try:
        name = request.json.get('name')
        retrieveSql = f'''
            insert into `Kits` (`name`) values ('{name}')
        '''
        g.CURSOR.execute(retrieveSql)
        
        return name
    except Error as e:
        return e.msg
