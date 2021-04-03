#!/usr/bin/env python3

import json
import schulen
import getAlleAdressen

def convert(adresse):
    return {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [ adresse['coord']['lon'], adresse['coord']['lat']  ]},
        'properties': {
            'address': adresse['name'],
            'naechste_insgesamt': adresse['naechste']['insgesamt']['name'],
            'naechste_insgesamt_distance': adresse['naechste']['insgesamt']['distance'],
            'naechste_insgesamt_typ': adresse['naechste']['insgesamt']['typ'],
            **{f'naechste_{category}_{k}': v for category, naechste_category in naechste.items()
                for k, v in naechste_category.items() if category != 'insgesamt' }}}

strassen_iterator = getAlleAdressen.getAllStrassen()
schulen.all_schools = schulen.lookup_schools()
with open('abstaende.geo.json','w') as f:
    f.write('{"type": "FeatureCollection","features":[')
    first = True
    for adresse in getAlleAdressen.getAllAdressenFromStrassen(strassen_iterator):
        naechste = schulen.nearest_by_coord(adresse['coord'])

        if not first:
            f.write(',')
        f.write(json.dumps(convert({ **adresse, 'naechste': naechste })))

        print(adresse['name'])
        naechste_schule = naechste['insgesamt']['name'] + ', eine ' + naechste['insgesamt']['typ']
        print(f'Die nächste Schule ist die {naechste_schule:40s} \
            mit einem Fußweg von {naechste["insgesamt"]["distance"]:.2f}km')
    f.write(']}')
