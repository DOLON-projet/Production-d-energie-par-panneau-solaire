import mariadb
from mariadb import Error
try:

    print("Try to connected to Mariadb Server")
    connection =  mariadb.connect(host='172.20.30.13',
                                  database='projet_pedagogique',
                                  user="admin",
                                  password="fourcade")

    cursor = connection.cursor()
    cursor.execute("show databases;")
    records = cursor.fetchall()
    print("Databases: ", records)
    db_info = connection.get_server_version()
    print("Connected to Mariadb Server version", db_info)

    if connection.server_status:
        cursor.close()
        connection.close()
        print("Mariadb connection is closed")



except Error as e:
    print("Error while connecting to Mariadb", e)

