import mysql.connector
from mysql.connector import Error


def create_connection():
    
    # with open('mysql_password.txt', 'r', encoding='utf-8-sig') as fp:
    #     mysql_password = fp.read().rstrip()

    connection = None
    try:
        connection = mysql.connector.connect(
            host='db',
            port=3306,
            user='user_name',
            passwd='password',
            database='feedback',
        )
        connection.autocommit = True
        print("Connection to MySQl DB successful")
    except Error as err:
        print(f"The error '{err}' occerred")
        raise err
    
    return connection
