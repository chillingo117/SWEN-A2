from flask import Flask, Blueprint, g, request
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

generalInformationApi = Blueprint('generalInformationApi', __name__,  template_folder='templates')


@generalInformationApi.route("/organization", methods=['POST'])
def post_general_org_info():
    contactEmail = request.json.get('ContactEmail')
    contactName = request.json.get('ContactName')
    contactPhone = request.json.get('ContactPhone')
    organizationAddress = request.json.get('OrganizationAddress')
    organizationName = request.json.get('OrganizationName')

    try:
        sql = f'''
            insert into `Organizations` (`contactEmail`, `contactName`, `contactPhone`, `organizationAddress`, `organizationName`) values ('{contactEmail}', '{contactName}', '{contactPhone}', '{organizationAddress}', '{organizationName}')
        '''
        g.CURSOR.execute(sql)
        return contactName

    except Error as e:
        return e.msg

@generalInformationApi.route("/donor", methods=['POST'])
def post_general_donor_info():
    name = request.json.get('Name')
    age = request.json.get('Age')
    address = request.json.get('Address')
    email = request.json.get('Email')
    phone = request.json.get('Phone')
    preferredCommunication = request.json.get('CommunicationWay')

    try:
        sql = f'''
            insert into `Donors` (`name`, `age`, `address`, `email`, `phone`, `preferredCommunication`) values ('{name}', '{age}', '{address}', '{email}', '{phone}', '{preferredCommunication}')
        '''
        g.CURSOR.execute(sql)
        return 'yup'

    except Error as e:
        return e.msg

@generalInformationApi.route("/recipients", methods=['POST'])
def post_general_recipient_info():
    try:
        sql = f"""
        insert into `Recipients` (`age`, `name`, `phone`, `email`, `address`, `familySize`, `partnerAge`, `partnerName`, `kid1Age`, `kid1Name`, `kid2Age`, `kid2Name`, `kid3Age`, `kid3Name`) 
        values (%(AgeP)s, %(NameP)s, %(PhoneP)s, %(EmailP)s, %(Address)s, %(NumFa)s, %(AgePP)s, %(NamePP)s, %(AgeK1)s, %(NameK1)s, %(AgeK2)s, %(NameK2)s, %(AgeK3)s, %(NameK3)s)
    """
        g.CURSOR.execute(sql, request.json)
        return 'yup'

    except Error as e:
        return e.msg
