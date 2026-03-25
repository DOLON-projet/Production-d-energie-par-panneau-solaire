import requests
import time
import json   #importation de la bibliotèque json
while True:
    with open('test_transcript_json.json','r') as op:
        for line in op:
            # mise en place des données dans les variables correspondantes
            donnees = json.loads(line)
            tension_panneau_solaire = donnees['tP']
            tension_Batterie = donnees['tB']
            courant_panneau_solaire = donnees['cP']
            courant_Batterie = donnees['cB']
            temperature_armoire = donnees['tA']
            print("tension panneau : ", tension_panneau_solaire)
            print("tension baterie : ", tension_Batterie)
            print("courant panneau solaire : ", courant_panneau_solaire)
            print("courant batterie : ", courant_Batterie)
            print("temperature armoire : ", temperature_armoire)
            requests.post()
    time.sleep(10)