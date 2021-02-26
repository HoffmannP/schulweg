#!/usr/bin/env python3

import json
import schulen
import getAlleAdressen

strassenIterator = getAlleAdressen.getAllStrassen()

with open("abstaende.json","w") as f:
    f.write("[")
    for adresse in getAlleAdressen.getAllAdressenFromStrassen(strassenIterator):
        naechste = schulen.next_by_coord(adresse['coord'])
        f.write(json.dumps(adresse))
        f.write(',')
        print(adresse['name'])
        print(f'Die nächste Schule ist die {naechste["insgesamt"]["name"]}, eine {naechste["insgesamt"]["typ"]} mit einem Fußweg von {naechste["insgesamt"]["distance"]:.2f}km')
        print(f'Die nächste Grundschule ist die "{naechste["grundschulen"]["name"]}" mit einem Fußweg von {naechste["grundschulen"]["distance"]:.2f}km')
        print(f'Die nächste Gesamtschule ist die "{naechste["gesamtschulen"]["name"]}" mit einem Fußweg von {naechste["gesamtschulen"]["distance"]:.2f}km')
    f.write("{}]")