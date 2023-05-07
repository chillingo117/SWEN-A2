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

def dropDatabase():
    password = os.environ['SQL_PASSWORD']
    conn = connection.MySQLConnection(user='root', password=password)
    cursor = conn.cursor()

    dropDatabaseSql = ('''
        drop database if exists VR1Family
    ''')
    executeSql(dropDatabaseSql, "Dropping database", cursor, conn)

    cursor.close()
    conn.close()


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

def createAndPopulateKitsTable(cursor, conn):
    createKitsTableSql = ('''
        create table `Kits` (
            `id` int not null auto_increment,
            `name` nvarchar(50) unique,
            primary key (`id`)
        )
    ''')
    sqlDescription = 'Create Kits table'
    executeSql(createKitsTableSql, sqlDescription, cursor, conn)

    insertDefaultKitsSql = ("""
        insert into `Kits` (`name`) values ('{name}')
    """)
    sqlDescription = 'Insert default kit {} into Kits table'
    defaultKits = pd.read_csv(Path(__file__).parent / 'defaultData/default_kits.csv')

    for i, row in defaultKits.iterrows():
        executeSql(insertDefaultKitsSql.format(name=row[0]), sqlDescription.format(row[0]), cursor, conn)

def main():
    load_dotenv()
    dropDatabase()
    ensureVR1FamilySchemaExists()

    conn = connection.MySQLConnection(user='root', password=os.environ['SQL_PASSWORD'], database='VR1Family')
    cursor = conn.cursor()

    createAndPopulateKitsTable(cursor, conn)
    createAndPopulateCategoriesTable(cursor, conn)
    createAndPopulateItemsTable(cursor, conn)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()