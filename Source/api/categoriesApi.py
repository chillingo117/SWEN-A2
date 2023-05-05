from flask import Flask, Blueprint, g
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

