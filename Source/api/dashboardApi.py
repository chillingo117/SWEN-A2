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

@dashboardApi.route("/items/bottom5", methods=['GET'])
def get_bottom5_items():
    bottom5 = []
    try:
        retrieveSql = '''
            select
                name as `label`,
                amount as `num`
            from `AidItems`
            order by amount
            limit 5 
        '''
        g.CURSOR.execute(retrieveSql)

        bottom5 = []
        for (label, num) in g.CURSOR:
            bottom5.append({'label': label, 'num': num})

        return bottom5
    except Error as e:
        return e.msg

@dashboardApi.route("/items/top10", methods=['GET'])
def get_top10_items_distributed():
    top10 = []
    try:
        retrieveSql = '''
            select summed.label, summed.num from
                (select
                    AI.name as `label`,
                    sum(R.quantity) as `num`
                from `Requisitions` R 
                    left join `AidItems` AI on R.itemId = AI.id    
                group by AI.id) as summed
            order by num desc
            limit 10
        '''
        g.CURSOR.execute(retrieveSql)

        top10 = []
        for (label, num) in g.CURSOR:
            top10.append({'label': label, 'num': num})

        return top10
    except Error as e:
        return e.msg

@dashboardApi.route("/items/top5", methods=['GET'])
def get_top5_items_donated():
    top5 = []
    try:
        retrieveSql = '''
            select
                AI.name as `label`,
                sum(A.quantity) as `num`
            from `Acquisitions` A
                left join `AidItems` AI on A.itemId = AI.id             

            where A.date > date_add(CURDATE(), interval -90 day)
            group by AI.id
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


