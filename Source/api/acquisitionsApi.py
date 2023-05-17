from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from datetime import datetime
from constants import *
import os

acquisitionsApi = Blueprint('acquisitionsApi', __name__,  template_folder='templates')

@acquisitionsApi.route("/acquisition", methods=['POST'])
def make_acquisition():
    try:
        incrementSql = f'''
            update AidItems set amount = amount + %(quantity)s where id = %(selectedId)s
        '''
        g.CURSOR.execute(incrementSql, request.json)

        sql = f'''
            insert into Acquisitions (`itemId`, `quantity`, `date`) values (%(selectedId)s, %(quantity)s, NOW())
        '''        
        g.CURSOR.execute(sql, request.json)

        return ''
        
    except Error as e:
        return e.msg
    
@acquisitionsApi.route("/acquisitions/unassigned", methods=['GET'])
def get_unassigned_acquisitions():
    try:
        sql = f'''
            select 
                A.id as id, 
                AI.name as itemName, 
                A.quantity as quantity,
                A.date as date
            from Acquisitions A 
                left join AidItems AI
                on A.itemId = AI.id
            where A.donorId is null
        '''
        g.CURSOR.execute(sql)

        acquisitions = []
        for (id, itemName, quantity, date) in g.CURSOR:
            acquisitionDescription = f'{quantity} units of {itemName} on {date.strftime("%B %d, %Y")}'

            acquisitions.append(
                {
                    'id': id,
                    'description': acquisitionDescription
                }
            )

        return acquisitions
    except Error as e:
        return e.msg
    
    
@acquisitionsApi.route("/acquisitions", methods=['GET'])
def get_acquisitions():
    try:
        sql = f'''
            select 
                A.id as id, 
                AI.name as itemName, 
                D.name as donorName,
                A.quantity as quantity,
                A.date as date
            from Acquisitions A 
                left join AidItems AI
                on A.itemId = AI.id
                left join Donors D
                on A.donorId = D.id
            where A.donorId is not null
        '''
        g.CURSOR.execute(sql)

        acquisitions = []
        for (id, itemName, donorName, quantity, date) in g.CURSOR:
            acquisitions.append(
                {
                    'id': id,
                    'itemName': itemName,
                    'donorName': donorName,
                    'quantity': quantity,
                    'date': date.strftime("%B %d, %Y")
                }
            )

        return acquisitions
    except Error as e:
        return e.msg

@acquisitionsApi.route("/acquisitions/assign", methods=['POST'])
def assign_acquisition():
    try:
        sql = f'''
            update Acquisitions set donorId = %(donorId)s where id = %(acquisitionId)s
        '''
        g.CURSOR.execute(sql, request.json)

        return ''
        
    except Error as e:
        return e.msg