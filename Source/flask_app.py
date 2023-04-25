from flask import Flask
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
CONN = connection.MySQLConnection(user='root', password=os.environ['SQL_PASSWORD'], database='VR1Family')
CURSOR = CONN.cursor()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def get_test():
    try:
        retrieveSql = '''
            select * from TestTable;
        '''
        CURSOR.execute(retrieveSql)
        return list(CURSOR)
    except Error as e:
        return e.msg


@app.route("/categories")
def get_categories():
    categories = []
    try:
        retrieveSql = '''
            select AC.`id` as `id`, ac.`name` as `name`, sum(AI.`amount`) as `itemAmount` from `AidCategories` as AC left join `AidItems` as AI
            on AC.`id` = AI.`categoryId` group by AC.`id`
        '''
        CURSOR.execute(retrieveSql)

        for (id, name, itemAmount) in CURSOR:
            itemAmount = 0 if itemAmount == None else itemAmount
            categoryItemLevel='Unknown'
            if(itemAmount == CategoryItemLevels.NONE.value):
                categoryItemLevel = 'None'
            elif(itemAmount < CategoryItemLevels.LOW.value):
                categoryItemLevel = 'Low'
            elif(itemAmount < CategoryItemLevels.MEDIUM.value):
                categoryItemLevel = 'Medium'
            elif(itemAmount < CategoryItemLevels.HIGH.value):
                categoryItemLevel = 'High'
            else:
                categoryItemLevel = 'Excess'
            categories.append({'id': id, 'name': name, 'categoryItemLevel': categoryItemLevel})
        return categories
    except Error as e:
        return e.msg
