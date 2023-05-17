from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

recipientApi = Blueprint('recipientApi', __name__,  template_folder='templates')


@recipientApi.route("/recipients", methods=['GET'])
def get_recipients():
    try:
        sql = f"""
            select id, name from `Recipients`
        """
        g.CURSOR.execute(sql)
        recipients = []

        for id, name in g.CURSOR:
            recipients.append({'id': id, 'name':name})
        return recipients

    except Error as e:
        return e.msg
