import mariadb                             #lien avec la base de donné
from mariadb import Error                  #lien avec la bibliotèque d'erreur de mariadb
tension_batterie=12                        #initialisation de variables d'exemple
tension_du_panneau=10.5

try:

    print("Try to connected to Mariadb Server")                    #affichage textuelle de la connection à mariadb
    connection =  mariadb.connect(host='172.20.30.13',             #adresse de l'hôte
                                  database='projet_pedagogique',   #connection a la base de donné "projet_pedagogique"
                                  user="admin",                    #nom de l'utulisateur "admin"
                                  password="fourcade")             #mot de passe "fourcade"

    cursor = connection.cursor()          #création du de l'objet "cursor" qui permet la modification

    cursor.execute("INSERT INTO info_panneau (tension_batterie,tension_du_panneau) VALUES (?,?)" , (tension_batterie, tension_du_panneau))          #utilisation du cursor qui permet la creation des variable de temp etc...
    connection.commit()

    if connection.server_status:        #si la connection est fini alors fermer le curseur et la connection
        cursor.close()
        connection.close()


except Error as e:
    print("Error while connecting to Mariadb", e)      #si il y a une erreur à la connection à mariadb, alors afficher "Error while connecting to Mariadb"

