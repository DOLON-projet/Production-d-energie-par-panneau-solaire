import paho.mqtt.client as mqtt  # Importation de la bibliothèque pour la communication MQTT
import json                      # Pour manipuler les données au format JSON
import base64                    # Pour décoder les données venant de TTN (Base64)
import mariadb                   # Pour la connexion à la base de données MariaDB
from mariadb import Error        # Pour capturer les erreurs spécifiques à MariaDB

# --- 1. CHARGEMENT DES CONFIGURATIONS (SÉCURITÉ) ---
try:
    # Lecture du mot de passe de la base de données
    with open('mdp_BDD.json', 'r') as op:
        mot_de_passe = json.loads(op.read())['mdp_BDD']
        print("✅ mdp BDD chargé")

    # Lecture des identifiants API et réseau TTN
    with open('mdp_API_key.json', 'r') as op:
        data = json.loads(op.read())
        API_KEY = data['mdp_API_key']            # Clé API pour s'authentifier sur TTN
        DevEUI = data['DevEUI']                  # Identifiant unique du capteur
        APP_ID = data['ID']                      # Identifiant de l'application
        THINGS_NETWORK_URL = data['THINGS_NETWORK_URL'] # Adresse du serveur MQTT (ex: eu1.cloud...)
        usernamettn = data['client']             # Nom d'utilisateur MQTT
        print("✅ Identifiants TTN chargés")

except Exception as e:
    # Si un fichier est absent ou mal formé, on arrête le script
    print(f"❌ Erreur lecture fichiers config : {e}")
    exit()


# --- 2. FONCTION DE SAUVEGARDE EN BASE DE DONNÉES ---
def save_to_mariadb(info_panneaudb):
    """Reçoit un dictionnaire et l'insère dans la table info_panneau."""
    try:
        # Établissement de la connexion avec le serveur MariaDB
        connection = mariadb.connect(
            host='172.20.30.13',
            database='projet_pedagogique',
            user="admin",
            password=mot_de_passe
        )
        cursor = connection.cursor() # Création d'un curseur pour exécuter des commandes SQL

        # Préparation de la requête SQL d'insertion
        query = "INSERT INTO info_panneau (tension_panneau, courant_panneau) VALUES (?, ?)"
        
        # Exécution de la requête avec les données (tP = tension Panneau, cP = courant Panneau)
        cursor.execute(query, (float(info_panneaudb["tP"]), float(info_panneaudb["cP"])))
        
        connection.commit() # Validation de l'enregistrement dans la base
        cursor.close()      # Fermeture du curseur
        connection.close()  # Fermeture de la connexion
        print(f"💾 BDD : Données enregistrées (Tension: {info_panneaudb['tP']}V)")

    except Error as e:
        print(f"❌ Erreur MariaDB : {e}")


# --- 3. GESTION DES ÉVÉNEMENTS MQTT ---

def on_connect(client, userdata, flags, reason_code, properties):
    """Appelée lors de la connexion au serveur TTN."""
    print(f"🔗 Connecté avec le code : {reason_code}")
    # S'abonner à tous les messages de l'application
    client.subscribe("#")

def on_message(client, userdata, msg):
    """Appelée à chaque réception d'un nouveau message."""
    try:
        print("📩 Message reçu de TTN")
        
        # Décodage du JSON reçu dans le payload MQTT
        donnee_recues = json.loads(msg.payload.decode('utf-8'))
        
        # Extraction de la charge utile (payload) encodée en Base64
        payload_base64 = donnee_recues['uplink_message']['frm_payload']
        
        # Décodage Base64 vers binaire, puis conversion en chaîne hexadécimale
        valeurs_hex = base64.b64decode(payload_base64).hex()
        print(f"🔍 Data Hex : {valeurs_hex}")

        # Découpage de la chaîne hexadécimale (2 caractères = 1 octet)
        info_panneau = {}
        info_panneau["tP"] = int(valeurs_hex[0:2], 16)   # Octet 1 : Tension Panneau
        info_panneau["tB"] = int(valeurs_hex[2:4], 16)   # Octet 2 : Tension Batterie
        info_panneau["cP"] = int(valeurs_hex[4:6], 16)   # Octet 3 : Courant Panneau
        info_panneau["cB"] = int(valeurs_hex[6:8], 16)   # Octet 4 : Courant Batterie
        info_panneau["tA"] = int(valeurs_hex[8:10], 16)  # Octet 5 : Température Ambiante

        # Envoi des données vers la fonction de sauvegarde
        save_to_mariadb(info_panneau)
        print("--------------------------------------------------")

    except Exception as e:
        print(f"⚠️ Erreur lors du traitement du message : {e}")


# --- 4. LANCEMENT DU CLIENT MQTT ---

print("🚀 Lancement du bridge...")

# Initialisation du client MQTT avec la dernière version de l'API
mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

# Configuration des identifiants de connexion TTN
mqttc.username_pw_set(username=usernamettn, password=API_KEY)

# Attribution des fonctions de rappel (callbacks)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connexion au serveur TTN sur le port 1883
mqttc.connect(THINGS_NETWORK_URL, 1883, 60)

# Lancement de la boucle infinie pour écouter les messages
mqttc.loop_forever()
