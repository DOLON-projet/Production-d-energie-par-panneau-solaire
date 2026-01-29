import json
with open('test_transcript_json.json','r') as op:
    read_data = op.read()
    op.close()

donnees = json.loads(read_data)
tension_panneau_solaire = donnees['tP']
tension_Batterie = donnees['tB']
courant_panneau_solaire = donnees['cP']
courant_Batterie = donnees['cB']
temperature_armoire = donnees['tA']
print(tension_panneau_solaire)
print(tension_Batterie)
print(courant_panneau_solaire)
print(courant_Batterie)
print(temperature_armoire)
