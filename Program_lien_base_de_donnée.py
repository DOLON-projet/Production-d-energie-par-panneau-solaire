from pickletools import uint8
import paho.mqtt.client as mqtt
import json
import base64
import mariadb
from mariadb import Error


# --- CHARGEMENT DES MOTS DE PASSE ---
try:
    with open('mdp_BDD.json', 'r') as op:
        mot_de_passe = json.loads(op.read())['mdp_BDD']
        print("mdp BDD charge")
    with open('mdp_API_key.json', 'r') as op:
        data = json.loads(op.read())
        mot_de_passe_API =data['mdp_API_key']
        print("mdp API_key charge")
        mot_de_passe_API2 = data['DevEUI']
        print("mdp DevEUI charge")
        mot_de_passe_API3 = data['ID']
        print("mdp ID")
        mot_de_passe_API4 = data['THINGS_NETWORK_URL']
        print("mdp THINGS_NETWORK_URL")
        mot_de_passe_API5 = data['client']
        print("id client")
except Exception as e:
    print(f"❌ Erreur lecture fichiers config : {e}")
    exit()

# --- CONFIGURATION TTN (CORRIGÉE) ---
# L'adresse doit être UNIQUEMENT le serveur, pas le lien de la console
THINGS_NETWORK_URL = mot_de_passe_API4
APP_ID = mot_de_passe_API3
API_KEY = mot_de_passe_API
DevEUI = mot_de_passe_API2
usernamettn = mot_de_passe_API5




print("🚀 Lancement du bridge...")
try:

    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("#")


        # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print("message reçu")
        donnee_recues = json.loads(str(msg.payload.decode('utf-8')))
        print(donnee_recues['uplink_message']['frm_payload'])
        encoded = str(donnee_recues['uplink_message']['frm_payload'])
        encoded = str(base64.b64decode(encoded))
        print(encoded)
        #donnee = json.loads(str(base64.b64decode(encoded)))
       # print(donnee)
        print("##########################################################################")


    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(username=usernamettn, password=API_KEY)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(THINGS_NETWORK_URL, 1883, 60)
    mqttc.loop_forever()


    def save_to_mariadb(tension_batt, tension_panneau):
        """Connexion et insertion dans MariaDB"""

        connection = mariadb.connect(
            host='172.20.30.13',
            database='projet_pedagogique',
            user="admin",
            password=mot_de_passe
            )
        cursor = connection.cursor()
        query = "INSERT INTO info_panneau (tension_batterie, tension_du_panneau) VALUES (?, ?)"
        cursor.execute(query, (float(tension_batt), float(tension_panneau)))
        connection.commit()
        cursor.close()
        connection.close()
        print(f"✅ BDD : Batt={tension_batt}V, Panneau={tension_panneau}V")
except Error as e:
        print("❌ Erreur MariaDB :", e)





