import time
import json
import serial

# --- Configuration du module LoRa-E5 ---
PORT_SERIE = '/dev/ttyS0'  # GPIO 14 (TX) et 15 (RX) sur Raspberry Pi
BAUD_RATE = 9600  # Par défaut sur LoRa-E5
ser = serial.Serial(PORT_SERIE, BAUD_RATE, timeout=2)


def send_at(command, wait=1):
    """Envoie une commande AT et retourne la réponse du module"""
    cmd = command + "\r\n"
    ser.write(cmd.encode())
    time.sleep(wait)
    response = ""
    while ser.in_waiting:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(f"Module LoRa-E5 : {line}")
            response += line
    return response


def envoyer_donnees_lora(donnees):
    """Convertit les données en hexadécimal et les envoie via AT+MSGHEX"""
    try:
        payload_hex = ""
        # On parcourt tes clés de capteurs
        for cle in ['tP', 'tB', 'cP', 'cB', 'tA']:
            valeur = int(donnees[cle])
            # On s'assure que la valeur est entre 0 et 255 (1 octet)
            # :02X transforme 25 en '19'
            payload_hex += f"{valeur:02X}"

        print(f"Préparation Payload (Hexa) : {payload_hex}")

        # Sur LoRa-E5, la commande est AT+MSGHEX="XXXX"
        send_at(f'AT+MSGHEX="{payload_hex}"', wait=2)

    except Exception as e:
        print(f"Erreur formatage ou envoi : {e}")


# --- Initialisation et Connexion TTN ---
print("--- Initialisation du module Seeed LoRa-E5 ---")
send_at("AT")  # Test de présence
send_at("AT+ID")  # Affiche DevEUI pour vérification TTN
send_at("AT+MODE=LWOTAA")  # S'assure d'être en mode OTAA
send_at("AT+DR=EU868")  # Région Europe

print("\nTentative de JOIN (Connexion à TTN)...")
# Note : Le JOIN peut prendre plusieurs secondes
send_at("AT+JOIN", wait=5)

try:
    print("\nDébut de la lecture du fichier JSON...")
    while True:
        try:
            with open('test_transcript_json.json', 'r') as op:
                for line in op:
                    if not line.strip(): continue

                    donnees_brutes = json.loads(line)
                    print(f"\nDonnées lues : {donnees_brutes}")

                    # Envoi vers TTN
                    envoyer_donnees_lora(donnees_brutes)

                    # IMPORTANT : Respect du Duty Cycle LoRaWAN (1% de temps de parole)
                    # Pour 5 octets, 20 à 30 secondes d'attente est un minimum raisonnable
                    print("Attente avant prochain envoi...")
                    time.sleep(30)

        except FileNotFoundError:
            print("Fichier 'test_transcript_json.json' non trouvé...")
            time.sleep(10)
except KeyboardInterrupt:
    print("\nArrêt par l'utilisateur...")
finally:
    ser.close()