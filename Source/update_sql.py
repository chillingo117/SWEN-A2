from mysql.connector import connection, errorcode, Error

def main():
    conn = connection.MySQLConnection(user='root', password='swen',
                                    host='127.0.0.1',
                                    database='swen')
    cursor = conn.cursor()

    TABLES = {}
    TABLES['TestTable'] = ( '''
        create table TestTable (
            test_col varchar(10)
        )
    ''')

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()