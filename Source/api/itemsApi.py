from flask import Flask, Blueprint, g
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

itemsApi = Blueprint('itemsApi', __name__,  template_folder='templates')


@itemsApi.route("/items", methods=['GET'])
def get_items():
    itemsApi = []
    try:
        retrieveSql = '''
            select * from `AidItems`
        '''
        g.CURSOR.execute(retrieveSql)

        items = []
        for (id, name, amount, categoryId) in g.CURSOR:
            items.append({'id': id, 'name': name, 'amount': amount, 'categoryId': categoryId})

        return items
    except Error as e:
        return e.msg

