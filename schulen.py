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

def schools(typus):
    if this.all_schools is False:
        with open('schulen.json', "r") as f:
            this.all_schools = json.load(f)
    return this.all_schools[typus]


def nearest_by_type(start, typus):
    nearest = {"distance": 9999999}
    for school, end in schools(typus).items():
        if coordinates.entfernungLuft(start, end) > nearest["distance"]:
            continue
        distance = coordinates.entfernungFuss(start, end)
        if distance < nearest["distance"]:
            nearest["distance"] = distance
            nearest["name"] = school
    return nearest


def nearest(home):
    return nearest_by_coord(coordinates.getCoordinate(home))


def nearest_by_coord(start):
    nearest_grund = nearest_by_type(start, 'Grundschulen')
    nearest_gms = nearest_by_type(start, 'Gesamtschulen')
    if nearest_grund["distance"] < nearest_gms["distance"]:
        nearest = {**nearest_grund, 'typ': 'Grundschulen'}
    else:
        nearest = {**nearest_gms, 'typ': 'Gesamtschulen'}
    return {
        'insgesamt': nearest,
        'grundschulen': nearest_grund,
        'gesamtschulen': nearest_gms}


if __name__ == "__main__":
    print(nearest(sys.argv[1]))
