from flask import Flask, Blueprint, g
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

dashboardApi = Blueprint('dashboardApi', __name__,  template_folder='templates')


@dashboardApi.route("/categories/top5", methods=['GET'])
def get_top5():
    top5 = []
    try:
        retrieveSql = '''
            select
                AC.name as `label`,
                sum(R.quantity) as `num`
            from `Requisitions` R 
                left join `AidItems` AI on R.itemId = AI.id             
                left join `AidCategories` AC on AI.categoryId = AC.id 
                
            where R.date > date_add(CURDATE(), interval -90 day)
            group by AC.id
            order by num desc
            limit 5;
        '''
        g.CURSOR.execute(retrieveSql)

        top5 = []
        for (label, num) in g.CURSOR:
            top5.append({'label': label, 'num': num})

        return top5
    except Error as e:
        return e.msg

