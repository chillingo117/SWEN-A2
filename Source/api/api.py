from flask import Flask, Blueprint
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

from api.categoriesApi import categoriesApi
from api.itemsApi import itemsApi
from api.kitsApi import kitsApi
from api.dashboardApi import dashboardApi
from api.requisitionsApi import requisitionsApi
from api.generalInformationApi import generalInformationApi
from api.acquisitionsApi import acquisitionsApi
from api.loginApi import loginApi
from api.donorsApi import donorsApi

api = Blueprint('api', __name__,  template_folder='templates')
api.register_blueprint(categoriesApi)
api.register_blueprint(itemsApi)
api.register_blueprint(kitsApi)
api.register_blueprint(dashboardApi)
api.register_blueprint(requisitionsApi)
api.register_blueprint(generalInformationApi)
api.register_blueprint(acquisitionsApi)
api.register_blueprint(loginApi)
api.register_blueprint(donorsApi)
