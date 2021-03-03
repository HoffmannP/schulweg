#!/usr/bin/env python3

import json
import schulen
import getAlleAdressen

strassen_iterator = getAlleAdressen.getAllStrassen()

with open("abstaende.json","w") as f:
    f.write("[")
    for adresse in getAlleAdressen.getAllAdressenFromStrassen(strassen_iterator):
        naechste = schulen.nearest_by_coord(adresse['coord'])
        f.write(json.dumps(adresse))
        f.write(',')
        print(adresse['name'])
        naechste_schule = naechste['insgesamt']['name'] + ', eine ' + naechste['insgesamt']['typ']
        print(f'Die nächste Schule ist die {naechste_schule:40s} \
            mit einem Fußweg von {naechste["insgesamt"]["distance"]:.2f}km')
        print(f'Die nächste Grundschule ist die {naechste["grundschulen"]["name"]:35s} \
            mit einem Fußweg von {naechste["grundschulen"]["distance"]:.2f}km')
        print(f'Die nächste Gesamtschule ist die {naechste["gesamtschulen"]["name"]:34s} \
            mit einem Fußweg von {naechste["gesamtschulen"]["distance"]:.2f}km')
    f.write("{}]")