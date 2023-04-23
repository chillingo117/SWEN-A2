from mysql.connector import (connection)

conn = connection.MySQLConnection(user='root', password='swen',
                                 host='127.0.0.1',
                                 database='swen')

