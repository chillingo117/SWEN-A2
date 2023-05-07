from flask import Flask, Blueprint, g, request
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

@itemsApi.route("/item/create", methods=['POST'])
def create_item():
    try:
        sql = f"""
            insert into `AidItems` (`name`, `amount`, `categoryId`, `extraInfo`) values (%(name)s, %(quantity)s, %(categoryId)s, %(extraInfo)s)
        """
        g.CURSOR.execute(sql, request.json)
        return 'item created successfully'

    except Error as e:
        return e.msg
