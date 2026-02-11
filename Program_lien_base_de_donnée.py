import mariadb
from mariadb import Error
tension_batterie=17.5
tension_du_panneau=12.5

try:

    print("Try to connected to Mariadb Server")
    connection =  mariadb.connect(host='172.20.30.13',
                                  database='projet_pedagogique',
                                  user="admin",
                                  password="fourcade")

    cursor = connection.cursor()

    cursor.execute("INSERT INTO info_panneau (tension_batterie,tension_du_panneau) VALUES (?,?)" , (tension_batterie, tension_du_panneau))
    connection.commit()

    if connection.server_status:
        cursor.close()
        connection.close()
        print("Mariadb connection is closed")


except Error as e:
    print("Error while connecting to Mariadb", e)

