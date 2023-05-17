from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

privateInformationApi = Blueprint('privateInformationApi', __name__,  template_folder='templates')

    
@privateInformationApi.route("/donors/pi", methods=['POST'])
def post_donor_pi():
    try:
        sql = f'''
            insert into `DonorPI` (`donorId`, `nationality`, `docName`, `docId`, `docExpiry`) values (%(donorId)s, %(nationality)s, %(docName)s, %(docId)s, %(docExpiry)s)
        '''
        g.CURSOR.execute(sql, request.json)

        return 'posted'
    except Error as e:
        return e.msg


@privateInformationApi.route("/recipients/pi", methods=['POST'])
def post_recipient_pi():
    try:
        sql = f'''
            insert into `RecipientPI` (`recipientId`, `nationality`, `docName`, `docId`, `docExpiry`) values (%(recipientId)s, %(nationality)s, %(docName)s, %(docId)s, %(docExpiry)s)
        '''
        g.CURSOR.execute(sql, request.json)

        return 'posted'
    except Error as e:
        return e.msg
