from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from datetime import datetime
from constants import *
import os

requisitionsApi = Blueprint('requisitionsApi', __name__,  template_folder='templates')

@requisitionsApi.route("/requisition", methods=['POST'])
def make_requisition():
    try:
        selectedId = request.json.get('selectedId')
        quantity = request.json.get('quantity')
        note = request.json.get('note')
        isSelectingKit = request.json.get('isSelectingKit')
        date = datetime.now().isoformat()

        insertSql = ''

        if isSelectingKit:
            insertSql = f'''
                insert into `Distribution` (`kitId`, `quantity`, `note`, `date`) values ({selectedId}, {quantity}, '{note}', '{date}')
            '''
        else:
            insertSql = f'''
                insert into `Distribution` (`itemId`, `quantity`, `note`, `date`) values ({selectedId}, {quantity}, '{note}', '{date}')
            '''
        g.CURSOR.execute(insertSql)
        
        return ''
    except Error as e:
        return e.msg
