from mysql.connector import connection, errorcode, Error
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import os

def executeSql(sqlString, sqlDescription, cursor, conn):
    try:
        print(sqlDescription)
        cursor.execute(sqlString)
        conn.commit()
    except Error as err:
        print(err.msg)
        conn.rollback()
    else:
        print("OK")
        conn.rollback()

def ensureVR1FamilySchemaExists():
    password = os.environ['SQL_PASSWORD']
    conn = connection.MySQLConnection(user='root', password=password)
    cursor = conn.cursor()

    createDatabaseSql = ('''
        create database VR1Family;
    ''')
    sqlDescription = 'creating VR1Family database'
    executeSql(createDatabaseSql, sqlDescription, cursor, conn)

    cursor.close()
    conn.close()

def createAndPopulateCategoriesTable(cursor, conn):
    createCategoriesTableSql = ('''
        create table `AidCategories` (
            `id` int not null auto_increment,
            `name` nvarchar(50) unique,
            primary key (`id`)
        )
    ''')
    sqlDescription = 'Create AidCategories table'
    executeSql(createCategoriesTableSql, sqlDescription, cursor, conn)

    insertDefaultCategoriesSql = ("""
        insert into `AidCategories` (`name`) values ('{name}')
    """)
    sqlDescription = 'Insert default category {} into AidCategories table'
    defaultCategories = pd.read_csv(Path(__file__).parent / 'defaultData/default_categories.csv')

    for i, row in defaultCategories.iterrows():
        executeSql(insertDefaultCategoriesSql.format(name=row[0]), sqlDescription.format(row[0]), cursor, conn)

def createAndPopulateItemsTable(cursor, conn):
    createItemsTableSql = ('''
        create table `AidItems` (
            `id` int not null auto_increment,
            `name` nvarchar(50) unique,
            `amount` int default 0,
            `categoryId` int,
            primary key (`id`),
            foreign key (`categoryId`) references `AidCategories`(`id`)
        )
    ''')
    sqlDescription = 'Create AidItems table'
    executeSql(createItemsTableSql, sqlDescription, cursor, conn)

    insertDefaultItemsSql = ("""
        insert into `AidItems` (`name`, `amount`, `categoryId`) values ('{name}', {amount}, {categoryId})
    """)
    sqlDescription = 'Inserting item into AidItems table'
    defaultCategories = pd.read_csv(Path(__file__).parent / 'defaultData/default_items.csv')

    for i, row in defaultCategories.iterrows():
        executeSql(insertDefaultItemsSql.format(name=row[0], amount=row[1], categoryId=row[2]), sqlDescription, cursor, conn)

def createAndPopulateTestTable(cursor, conn):
    createTestTableSql = ( '''
        create table TestTable (
            id int,
            test_col varchar(10),
            primary key (id)
        );
    ''')
    sqlDescription = 'creating TestTable'

    executeSql(createTestTableSql, sqlDescription, cursor, conn)

    insertTestDataSql = ('''
        insert into TestTable (id, test_col) values ({}, '{}');
    ''')
    sqlDescription='inserting test data'
    executeSql(insertTestDataSql, sqlDescription, cursor, conn)

def main():
    load_dotenv()
    ensureVR1FamilySchemaExists()

    conn = connection.MySQLConnection(user='root', password=os.environ['SQL_PASSWORD'], database='VR1Family')
    cursor = conn.cursor()

    createAndPopulateTestTable(cursor, conn)
    createAndPopulateCategoriesTable(cursor, conn)
    createAndPopulateItemsTable(cursor, conn)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()