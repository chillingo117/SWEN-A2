from flask import Flask, Blueprint
from flask_cors import CORS
from mysql.connector import connection, Error
from dotenv import load_dotenv
from constants import *
import os

from api.categoriesApi import categoriesApi
from api.itemsApi import itemsApi

api = Blueprint('api', __name__,  template_folder='templates')
api.register_blueprint(categoriesApi)
api.register_blueprint(itemsApi)
