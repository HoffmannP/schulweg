#!/usr/bin/env python3

import requests
import math
import json
from pyproj import Transformer

HOST = 'http://localhost:5000'

def getCoordinateFromBbox(bbox):
    return [(bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2]

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


def OSM_LongLat(osm):
    transformer = Transformer.from_crs("epsg:5972", "epsg:4326")
    return transformer.transform(osm[0], osm[1])


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


def naechsteSchule(homeCo, schulen):
    naechste = {"distanz": 99999999}
    zweitnaechste = {}
    for schule, schoolCo in schulen.items():
        distanz = math.sqrt((homeCo[0] - schoolCo[0])**2 + (homeCo[1] - schoolCo[1])**2)
        if distanz < naechste["distanz"]:
            zweitnaechste = dict(naechste)
            naechste["distanz"] = distanz
            naechste["name"] = schule
    return naechste, zweitnaechste


"""
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
"""

with open("schulen.json", "r") as f:
    schulen = json.load(f)

# home = "Hermann-Löns-Straße 77"
home = "Philosophenweg 28"
homeCo = getCoordinate(home)
# print(f'"{home}", {homeCo[0]}, {homeCo[1]}')

GMS = OSM_LongLat(schulen["Gesamtschulen"]["Wenigenjena"])
# print(f'"GMS Wenigenjena", {GMS[0]}, {GMS[1]}')

def entfernung(Point1, Point2):
    response = requests.get(
        f'{HOST}/route/v1/foot/{Point1[1]},{Point1[0]};{Point2[1]},{Point2[0]}',
        params={'overview': 'false', 'skip_waypoints': 'true'})
    return response.json()["routes"][0]["distance"] / 1000

distance = entfernung(homeCo, GMS)
print(f'Die Entfernung beträgt {distance:.2f}km')

"""
naechsteGS, zweitnaechsteGS = naechsteSchule(homeCo, schulen["Grundschulen"])
naechsteGMS, zweitnaechsteGMS = naechsteSchule(homeCo, schulen["Gesamtschulen"])

if naechsteGMS["distanz"] > naechsteGS["distanz"]:
    print(f"Die nächste Schule ist die '{naechsteGS['name']}'")
    if (zweitnaechsteGS["distanz"] < naechsteGMS["distanz"]):
        print(f"Die zweitnächste Schule ist die '{zweitnaechsteGS['name']}'")
        print(f"Die nächste Gesamtschule ist die '{naechsteGMS['name']}'")
    else:
        print(f"Die zweitnächste und nächste Gesamtschule ist die '{naechsteGMS['name']}'")
else:
    print(f"Die nächste Schule ist die '{naechsteGMS['name']}'")
    if (zweitnaechsteGMS["distanz"] < naechsteGS["distanz"]):
        print(f"Die zweitnächste Schule ist die '{zweitnaechsteGMS['name']}'")
        print(f"Die nächste Grundschule ist die '{naechsteGS['name']}'")
    else:
        print(f"Die zweitnächste und nächste Grundschule ist die '{naechsteGS['name']}'")

"""
