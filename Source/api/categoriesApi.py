from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

categoriesApi = Blueprint('categoriesApi', __name__,  template_folder='templates')


@categoriesApi.route("/categories", methods=['GET'])
def get_categories():
    categories = []
    try:
        retrieveSql = '''
            select AC.`id` as `id`, ac.`name` as `name`, sum(AI.`amount`) as `itemAmount` from `AidCategories` as AC left join `AidItems` as AI
            on AC.`id` = AI.`categoryId` group by AC.`id`
        '''
        g.CURSOR.execute(retrieveSql)

        for (id, name, itemAmount) in g.CURSOR:
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

@categoriesApi.route("/category/<categoryId>/items", methods=['GET'])
def get_category_items(categoryId):
    try:
        retrieveSql = f'''
            select * from `AidItems` where `categoryId` = {categoryId}
        '''
        g.CURSOR.execute(retrieveSql)
        
        items = []
        for (id, name, amount, categoryId) in g.CURSOR:
            items.append({'id': id, 'name': name, 'amount': amount, 'categoryId': categoryId})

        return items
    except Error as e:
        return e.msg



@categoriesApi.route("/categories/create", methods=['POST'])
def create_category():
    try:
        name = request.json.get('name')
        retrieveSql = f'''
            insert into `AidCategories` (`name`) values ('{name}')
        '''
        g.CURSOR.execute(retrieveSql)
        
        return name
    except Error as e:
        return e.msg
