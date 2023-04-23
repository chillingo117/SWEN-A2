from mysql.connector import connection, errorcode, Error
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    password = os.environ['SQL_PASSWORD']
    conn = connection.MySQLConnection(user='root', password=password)
    cursor = conn.cursor()

    createDatabaseSql = ('''
        create database VR1Family;
    ''')

    try:
        print('Creating VR1Family database')
        cursor.execute(createDatabaseSql)
    except Error as err:
            print(err.msg)
    else:
        print("OK")

    cursor.close()
    conn.close()

    conn = connection.MySQLConnection(user='root', password='swen', database='VR1Family')
    cursor = conn.cursor()

    createTestTableSql = ( '''
        create table TestTable (
            id int,
            test_col varchar(10),
            primary key (id)
        );
    ''')

    try:
        print("Creating table TestTable")
        cursor.execute(createTestTableSql)
    except Error as err:
        print(err.msg)
    else:
        print("OK")

    insertTestDataSql = ('''
        insert into TestTable (id, test_col) values (%s, %s);
    ''')

    try:
        print("Inserting test data")
        cursor.execute(insertTestDataSql, (3, 'test'))
        conn.commit() ##### DO NOT FORGET THIS #####
    except Error as err:
        print(err.msg)
    else:
        print("OK")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()