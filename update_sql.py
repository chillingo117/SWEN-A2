from mysql.connector import connection, errorcode, Error
from dotenv import load_dotenv
from pathlib import Path
import random
import math
from datetime import datetime, timedelta
import pandas as pd
import os

random.seed(1000)

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
            `name` nvarchar(50) unique not null,
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
            `name` nvarchar(50) unique not null,
            `amount` int not null default 0,
            `categoryId` int not null,
            `extraInfo` nvarchar(4000) default '',
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
        executeSql(insertDefaultItemsSql.format(name=row[0], amount=random.randint(0, 100), categoryId=row[1]), sqlDescription, cursor, conn)

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

def createAndPopulateKitItemRelationshipTable(cursor, conn):
    createTableSql = ('''
        create table `KitItemRelationship` (
            `id` int not null auto_increment,
            `itemId` int not null,
            `kitId` int not null,
            `quantity` int not null,
            primary key (`id`),
            foreign key (`itemId`) references `AidItems`(`id`),
            foreign key (`kitId`) references `Kits`(`id`)
        )
    ''')
    sqlDescription = 'Create Kits table'
    executeSql(createTableSql, sqlDescription, cursor, conn)

    insertDefaultsSql = ("""
        insert into `KitItemRelationship` (`itemId`, `kitId`, `quantity`) values ('{itemId}', '{kitId}', '{quantity}')
    """)
    sqlDescription = 'Insert default relationship to kits item relations table'
    defaultRelations = pd.read_csv(Path(__file__).parent / 'defaultData/default_kit-item_relationships.csv')

    for i, row in defaultRelations.iterrows():
        executeSql(insertDefaultsSql.format(itemId=row[0], kitId=row[1], quantity=row[2]), sqlDescription, cursor, conn)

def createAndPopulateRequisitionsTable(cursor, conn):
    createRequistionsTableSql = ('''
        create table `Requisitions` (
            `id` int not null auto_increment,
            `itemId` int,
            `kitId` int,
            `quantity` int not null,
            `note` nvarchar(4000) default "",
            `date` datetime not null,
            primary key (`id`),
            foreign key (`itemId`) references `AidItems`(`id`)
        )
    ''')
    sqlDescription = 'Create Requistions table'
    executeSql(createRequistionsTableSql, sqlDescription, cursor, conn)

    insertDefaultRequistionsSql = ("""
        insert into `Requisitions` (`itemId`, `kitId`, `quantity`, `date`) values ({itemId}, {kitId}, {quantity}, '{date}')
    """)
    sqlDescription = 'Insert default Requistions into Requistions table'
    defaultRequistions = pd.read_csv(Path(__file__).parent / 'defaultData/default_requisitions.csv')

    for i, row in defaultRequistions.iterrows():
        itemId = row[0]
        if(math.isnan(itemId)):
            itemId = 'NULL'
        kitId = row[1]
        if(math.isnan(kitId)):
            kitId = 'NULL'
        date = datetime.now() - timedelta(days=random.randint(1, 90))
        date = date.isoformat()

        executeSql(insertDefaultRequistionsSql.format(itemId=itemId, kitId=kitId, quantity=random.randint(1, 20), date=date), sqlDescription, cursor, conn)

def createAndPopulateOrganizationTable(cursor, conn):
    createTableSql = ('''
        create table `Organizations` (
            `id` int not null auto_increment,
            `contactEmail` nvarchar(4000) not null,
            `contactName` nvarchar(4000) not null,
            `contactPhone` int not null,
            `organizationAddress` nvarchar(4000) not null,
            `organizationName` nvarchar(4000) not null,
            primary key (`id`)
        )
    ''')
    sqlDescription = 'Create Organization info table'
    executeSql(createTableSql, sqlDescription, cursor, conn)

    insertDefaultSql = ("""
        insert into `Organizations` (`contactEmail`, `contactName`, `contactPhone`, `organizationAddress`, `organizationName`) values ('{contactEmail}', '{contactName}', '{contactPhone}', '{organizationAddress}', '{organizationName}')
    """)
    sqlDescription = 'Insert default org into organization table'
    defaultOrganizations = pd.read_csv(Path(__file__).parent / 'defaultData/default_organizations.csv')

    for i, row in defaultOrganizations.iterrows():
        executeSql(insertDefaultSql.format(contactEmail=row[0], contactName=row[1], contactPhone=row[2], organizationAddress=row[3], organizationName=row[4]), sqlDescription, cursor, conn)

def createAndPopulateDonorsTable(cursor, conn):
    createTableSql = ('''
        create table `Donors` (
            `id` int not null auto_increment,
            `name` nvarchar(4000) not null,
            `age` int not null,
            `address` nvarchar(4000) not null,
            `email` nvarchar(4000) not null,
            `phone` int not null,
            `preferredCommunication` nvarchar(4000) not null,
            primary key (`id`)
        )
    ''')
    sqlDescription = 'Create Donors info table'
    executeSql(createTableSql, sqlDescription, cursor, conn)

    insertDefaultSql = ("""
        insert into `Donors` (`name`, `age`, `address`, `email`, `phone`, `preferredCommunication`) values ('{name}', '{age}', '{address}', '{email}', '{phone}', '{preferredCommunication}')
    """)
    sqlDescription = 'Insert default donor into Donors table'
    defaultOrganizations = pd.read_csv(Path(__file__).parent / 'defaultData/default_donors.csv')

    for i, row in defaultOrganizations.iterrows():
        executeSql(insertDefaultSql.format(name=row[0], age=row[1], address=row[2], email=row[3], phone=row[4], preferredCommunication=row[5]), sqlDescription, cursor, conn)

def createAndPopulateRecipientsTable(cursor, conn):
    createTableSql = ('''
        create table `Recipients` (
            `id` int not null auto_increment,
            `age` int not null,
            `name` nvarchar(300) not null,
            `phone` int not null,
            `email` nvarchar(4000) not null,
            `address` nvarchar(4000) not null,
            `familySize` int,
            `partnerAge` int,
            `partnerName` nvarchar(300),
            `kid1Age` int,
            `kid1Name` nvarchar(300),
            `kid2Age` int,
            `kid2Name` nvarchar(300),
            `kid3Age` int,
            `kid3Name` nvarchar(300),
            primary key (`id`)
        )
    ''')
    sqlDescription = 'Create Recipients info table'
    executeSql(createTableSql, sqlDescription, cursor, conn)

    insertDefaultSql = ("""
        insert into `Recipients` (`age`, `name`, `phone`, `email`, `address`, `familySize`, `partnerAge`, `partnerName`, `kid1Age`, `kid1Name`, `kid2Age`, `kid2Name`, `kid3Age`, `kid3Name`) 
        values ({randAge}, '{name}', {randNum}, '{email}', '{address}', {randFamSize}, {randAge}, '{partnerName}', {randKidAge}, '{kid1Name}', {randKidAge}, '{kid2Name}', {randKidAge}, '{kid3Name}' )
    """)
    sqlDescription = 'Insert default Recipient into Recipients table'
    defaultOrganizations = pd.read_csv(Path(__file__).parent / 'defaultData/default_recipients.csv')

    for i, row in defaultOrganizations.iterrows():
        executeSql(insertDefaultSql.format(randAge='RAND()*(50-30)+30', randNum='RAND()*(999999-111111)+1111111', randFamSize='RAND()*(999999-111111)+1111111', randKidAge='RAND()*(10-1)+1', name=row[0], email=row[1], address=row[2], partnerName=row[3], kid1Name=row[4], kid2Name=row[5], kid3Name=row[6]), sqlDescription, cursor, conn)

def main():
    load_dotenv()
    dropDatabase()
    ensureVR1FamilySchemaExists()

    conn = connection.MySQLConnection(user='root', password=os.environ['SQL_PASSWORD'], database='VR1Family')
    cursor = conn.cursor()

    createAndPopulateKitsTable(cursor, conn)
    createAndPopulateCategoriesTable(cursor, conn)
    createAndPopulateItemsTable(cursor, conn)
    createAndPopulateRequisitionsTable(cursor, conn)
    createAndPopulateOrganizationTable(cursor, conn)
    createAndPopulateDonorsTable(cursor, conn)
    createAndPopulateRecipientsTable(cursor, conn)
    createAndPopulateKitItemRelationshipTable(cursor, conn)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()