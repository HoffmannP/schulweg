#!/usr/bin/env python3

import requests
import math
import json
from pyproj import Transformer

HOST = 'http://localhost:5000'

def getCoordinateFromBbox(bbox):
    return [(bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2]


def OSM_LongLat(osm):
    transformer = Transformer.from_crs("epsg:5972", "epsg:4326")
    latlon = transformer.transform(osm[0], osm[1])
    return {'lon': latlon[1], 'lat': latlon[0]}


"""
def getAdressenInStrasse(strasse):
    response = requests.get(
    url="https://mapfinder.jena.de/search",
    params={
        "query":                    strasse,
            "searchTables":         [],
            "searchFilters":        [],
            "searchArea":           "Jena",
            "searchCenter":         "",
            "searchRadius":         "",
            "topic":                "stadtplan",
            "resultLimit":          500,
            "resultLimitCategory":  5})

    print(response.json())
    return [{"Adresse": adresse["displaytext"].replace(" (Adresse)", ""), "Koordinaten": getCoordinateFromBbox(adresse["bbox"])} for adresse in filter(
        lambda hit: ("search_category" in hit) and (hit["search_category"] == "05_Adressen"),
        response.json()["results"])]
"""


def getCoordinate(address):
    response = requests.get(
        url="https://mapfinder.jena.de/search",
        params={
            "query":                address,
            "searchTables":         [],
            "searchFilters":        [],
            "searchArea":           "Jena",
            "searchCenter":         "",
            "searchRadius":         "",
            "topic":                "stadtplan",
            "resultLimit":          5,
            "resultLimitCategory":  5})

    adressen = [a for a in filter(
        lambda hit: ("search_category" in hit) and (
            hit["search_category"] == "05_Adressen"),
        response.json()["results"])]

    if len(adressen) == 0:
        raise Exception(f"Can't find the adress '{address}'")
    if len(adressen) > 3:
        raise Exception(f"Can't find one distinct adress for '{address}'")

    return OSM_LongLat(getCoordinateFromBbox(adressen[0]["bbox"]))


def deg2rad(deg):
    return deg * math.pi/180


def entfernungLuft(p1, p2):
    RADIUS = 6371
    dLat = deg2rad(p2['lat'] - p1['lat'])
    dLon = deg2rad(p2['lon'] - p1['lon'])
    a = math.sin(dLat/2)**2 + math.cos(deg2rad(p1['lat'])) * math.cos(
        deg2rad(p2['lat'])) * math.sin(dLon/2)**2
    return RADIUS * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def entfernungFuss(p1, p2):
    response = requests.get(
        f'{HOST}/route/v1/foot/{p1["lon"]},{p1["lat"]};{p2["lon"]},{p2["lat"]}',
        params={'overview': 'false', 'skip_waypoints': 'true'})
    return response.json()["routes"][0]["distance"] / 1000


def naechsteSchule(homeCoo, schulen):
    naechste = {"distanz": 999}
    for schule, schulCoo in schulen.items():
        if entfernungLuft(homeCoo, schulCoo) > naechste["distanz"]:
            # print(f"Luftentfernung {entfernungLuft(homeCoo, schulCoo):.2f}km")
            continue
        distanz = entfernungFuss(homeCoo, schulCoo)
        if distanz < naechste["distanz"]:
            # print(f"neuste Fußentfernung {distanz:.2f}km")
            naechste["distanz"] = distanz
            naechste["name"] = schule
    return naechste

def saveCoordinates():
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
        Grundschulen[schule] = getCoordinate(addresse)
    Gesamtschulen = {}
    for schule, addresse in schulenInJena["staatliche"]["Gesamtschulen"].items():
        Gesamtschulen[schule] = getCoordinate(addresse)
    with open("schulen.json", "w") as f:
        json.dump({
            "Grundschulen": Grundschulen,
            "Gesamtschulen": Gesamtschulen}, f)



with open("schulen.json", "r") as f:
    schulen = json.load(f)

home = "Philosophenweg 28"  # "Hermann-Löns-Straße 77"
homeCo = getCoordinate(home)

naechsteGS = naechsteSchule(homeCo, schulen["Grundschulen"])
naechsteGMS = naechsteSchule(homeCo, schulen["Gesamtschulen"])
naechsteSchule = { **naechsteGS, 'typ': 'GS' } if naechsteGS["distanz"] < naechsteGMS["distanz"] else { **naechsteGMS, 'typ': 'GMS' }

print(f'Die nächste Grundschule ist die "{naechsteGS["name"]}" mit einem Fußweg von {naechsteGS["distanz"]:.2f}km')
print(f'Die nächste Gesamtschule ist die "{naechsteGMS["name"]}" mit einem Fußweg von {naechsteGMS["distanz"]:.2f}km')
print(f'Die nächste Schule ist die {naechsteSchule["name"]}, eine {naechsteSchule["typ"]} mit einem Fußweg von {naechsteSchule["distanz"]:.2f}km')
