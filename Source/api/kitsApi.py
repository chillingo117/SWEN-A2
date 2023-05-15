from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import math
import os

kitsApi = Blueprint('kitsApi', __name__,  template_folder='templates')


@kitsApi.route("/kits", methods=['GET'])
def get_kits():
    kits = []
    try:
        getKitIds = '''
            select distinct id, name from Kits
        '''

        g.CURSOR.execute(getKitIds)
        for (id, name) in g.CURSOR:
            kits.append((id, name))

        retrieveSql = '''
            select K.id as kitId, K.name as kitName, AI.amount as itemsAvailable, R.quantity as itemsPerKit
            from `Kits` K 
                inner join KitItemRelationship R on K.id = R.kitId
                inner join AidItems AI on R.itemId = AI.id
        '''
        g.CURSOR.execute(retrieveSql)
        relations = []

        for (kitId, kitName, itemsAvailable, itemsPerKit) in g.CURSOR:
            relations.append({'kitId': kitId, 'kitName': kitName, 'itemsAvailable': itemsAvailable, 'itemsPerKit': itemsPerKit})

        kitsAvailable = []
        for kitId, kitName in kits:
            kitComponents = [relation for relation in relations if relation['kitId'] == kitId]
            maxKits = math.inf
            if(len(kitComponents) > 0):
                for kitComponent in kitComponents:
                    componentsAvailable = math.floor(kitComponent['itemsAvailable'] / kitComponent['itemsPerKit'])
                    maxKits = min(componentsAvailable, maxKits)
            else:
                maxKits = 0

            kitsAvailable.append({'kitId': kitId, 'kitName': kitName, 'numKits': maxKits})

        return kitsAvailable
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

@kitsApi.route("/kits/assign", methods=['POST'])
def assign_item_to_kit():
    try:
        sql = f'''
            insert into `KitItemRelationship` (`itemId`, `kitId`, `quantity`) values (%(itemId)s, %(kitId)s, %(quantity)s)
        '''
        g.CURSOR.execute(sql, request.json)
        
        return 'item assigned to kit'
    except Error as e:
        return e.msg
