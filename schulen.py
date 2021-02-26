import requests
import json
import coordinates
import sys

this = sys.modules[__name__]

def lookup_coordinates():
    schulenInJena = {
        "staatliche": {
            "Grundschulen": {
                "Friedrich-Schiller": "Hugo-Schrade-Straße 3",
                "Heinrich-Heine": "Dammstraße 37",
                "Nordschule": "Dornburger Straße 31",
                "Saaletalschule": "Karl-Marx-Allee 11",
                "Schule am Rautal": "Schreckenbachweg 3",
                "Südschule": "Döbereinerstraße 20",
                "Talschule": "Ziegenhainer Straße 52",
                "Westschule": "August-Bebel-Straße 23"},
            "Gesamtschulen": {
                "Werkstattschule": "Emil-Wölk-Str. 11",
                "An der Trießnitz": "Hugo-Schrade-Straße 1",
                "Galileo": "Oßmaritzer Straße 12",
                "Jenaplan-Schule": "Tatzendpromenade 9",
                "Kaleidoskop": "Karl-Marx-Allee 11",
                "Kulturanum": "Karl-Marx-Allee 7",
                "Lobdeburgschule": "Unter der Lobdeburg 4",
                "Montessorischule": "Friedrich-Wolf-Straße 2",
                "Wenigenjena": "Jenzigweg 29"}},
        "freie": {
            "Grundschulen": {
                "Dualingo": "Dammstraße 43",
                "Ev. Grundschule": "Kahlaische Straße 9",
                "SteinMalEins (Lobeda)": "Susanne-Bohl-Straße 2",
                "SteinMalEins (Paradies)": "Burgauer Weg 1a"},
            "Gesamtschulen": {
                "Leonardo": "Marie-Juchacz-Straße 1"}}}

    Grundschulen = {}
    for schule, addresse in schulenInJena["staatliche"]["Grundschulen"].items():
        Grundschulen[schule] = coordinates.getCoordinate(addresse)

    Gesamtschulen = {}
    for schule, addresse in schulenInJena["staatliche"]["Gesamtschulen"].items():
        Gesamtschulen[schule] = coordinates.getCoordinate(addresse)

    Schulen = {
        "Grundschulen": Grundschulen,
        "Gesamtschulen": Gesamtschulen}

    with open("schulen.json", "w") as f:
        json.dump(Schulen, f)
    return Schulen


all_schools = False

def schools(type):
    if this.all_schools is False:
        with open('schulen.json', "r") as f:
            this.all_schools = json.load(f)
    return this.all_schools[type]


def next_by_type(start, type):
    next = {"distance": 9999999}
    for school, end in schools(type).items():
        if coordinates.entfernungLuft(start, end) > next["distance"]:
            continue
        distance = coordinates.entfernungFuss(start, end)
        if distance < next["distance"]:
            next["distance"] = distance
            next["name"] = school
    return next


def next(home):
    return next_by_coord(coordinates.getCoordinate(home))


def next_by_coord(start):
    next_grund = next_by_type(start, 'Grundschulen')
    next_gms = next_by_type(start, 'Gesamtschulen')
    if next_grund["distance"] < next_gms["distance"]:
        next = {**next_grund, 'typ': 'Grundschulen'}
    else:
        next = {**next_gms, 'typ': 'Gesamtschulen'}
    return {
        'insgesamt': next,
        'grundschulen': next_grund,
        'gesamtschulen': next_gms}


if __name__ == "__main__":
    import sys
    print(next(sys.argv[1]))
