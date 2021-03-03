#!/usr/bin/env python3

import json

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
            'naechste_grundschulen': adresse['naechste']['grundschulen']['name'],
            'naechste_grundschulen_distance': adresse['naechste']['grundschulen']['distance'],
            'naechste_gemeinschaftsschulen': adresse['naechste']['gemeinschaftsschulen']['name'],
            'naechste_gemeinschaftsschulen_distance': adresse['naechste']['gemeinschaftsschulen']['distance']}}


with open('abstaende.json','r') as input_file:
    adressen = json.load(input_file)
    with open('abstaende.geojson','w') as output_file:
        output_file.write('{"type": "FeatureCollection","features":[')
        output_file.write(json.dumps(convert(adressen[0])))
        for adresse in adressen[1:-1]:
            print(adresse['name'])
            output_file.write(',')
            output_file.write(json.dumps(convert(adresse)))
        output_file.write(']}')
