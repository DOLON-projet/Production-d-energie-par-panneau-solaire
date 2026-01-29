import mariadb
from mariadb import Error
try:

    print("Try to connected to Mariadb Server")
    connection =  mariadb.connect(host='172.20.30.13',
                                  database='projet_pedagogoique',
                                  user="admin",
                                  password="fourcade")
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You are connected to database: ", record)

    cursor = connection.cursor()
    cursor = execute("show databases;")
    records = cursor.fetchall()
    print("Databases: ", records)

    if connection.is_connected():
        cursor.closed()
        connection._closed()
        print("Mariadb connection is closed")
    db_info = connection.get_server_info()
    print("Connected to Mariadb Server version", db_info)


except Error as e:
    print("Error while connecting to Mariadb", e)

