#!/usr/bin/env python3

import requests
import json
from pyproj import Transformer
import string

DEFAULT_STRASSEN_SAVE = 'strassen.json'
DEFAULT_ADRESSEN_SAVE = 'adressen.json'

def getCoordinateFromBbox(bbox):
    return [(bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2]

def OSM_LongLat(osm):
    transformer = Transformer.from_crs("epsg:5972", "epsg:4326")
    lonLat = transformer.transform(osm[0], osm[1])
    return {
        'lon': lonLat[1],
        'lat': lonLat[0]}

def isAddress(a):
    return 'search_category' in a and a['search_category'] == '05_Adressen'

def isInStreet(a, street):
    return 'displaytext' in a and a['displaytext'].startswith(f'{street} ')

def formatAddress(a):
    return {
        'name': a['displaytext'][:-len(' (Adresse)')],
        'coord': OSM_LongLat(getCoordinateFromBbox(a['bbox']))
    }

def isStrasse(a):
    return 'search_category' in a and a['search_category'] == '01_Strassen'

def getAdressenInStrasse(strasse):
    response = requests.get(
    url="https://mapfinder.jena.de/search",
    params={
        'query':                strasse,
        'searchTables':         [],
        'searchFilters':        [],
        'searchArea':           'Jena',
        'searchCenter':         '',
        'searchRadius':         '',
        'topic':                'stadtplan',
        'resultLimit':          500,
        'resultLimitCategory':  5})

    return [formatAddress(a) for a in response.json()["results"][1:] if isAddress(a) and isInStreet(a, strasse)]

def getStrassen(letter):
    response = requests.get(
    url="https://mapfinder.jena.de/search",
    params={
        'query':                letter,
        'searchTables':         [],
        'searchFilters':        [],
        'searchArea':           'Jena',
        'searchCenter':         '',
        'searchRadius':         '',
        'topic':                'stadtplan',
        'resultLimit':          500,
        'resultLimitCategory':  5})

    return [a['displaytext'][:-len(" (Strasse)")] for a in response.json()["results"][1:] if isStrasse(a)]

def getAddresse(address):
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
    adressen = list(filter(
        lambda a: ("search_category" in a) and (a["search_category"] == "05_Adressen"),
        response.json()["results"]))

    if len(adressen) == 0:
        raise Exception(f"Can't find the adress '{address}'")
    if len(adressen) > 3:
        raise Exception(f"Can't find one distinct adress for '{address}'")

    return OSM_LongLat(getCoordinateFromBbox(adressen[0]["bbox"]))

def getAllStrassen():
    strassen = []
    for letter in string.ascii_uppercase:
        for strasse in getStrassen(letter):
            if strasse not in strassen:
                yield strasse
                strassen.append(strasse)

def saveAllStrassen(filename=DEFAULT_STRASSEN_SAVE):
    with open(filename, "w") as f:
        json.dump(list(getAllStrassen()), f)

def loadAllStrassen(filename=DEFAULT_STRASSEN_SAVE):
    with open(filename, "r") as f:
        strassen = json.load(f)
    return strassen

def getAllAdressenFromStrassen(strassen):
    for strasse in strassen:
        adressenInStrasse = getAdressenInStrasse(strasse)
        print(f'{strasse}: {len(adressenInStrasse):3d} Adressen')
        for adresse in adressenInStrasse:
            yield adresse

def saveAllAdressenFromStrassen(strassen, database):
    for adresse in getAllAdressenFromStrassen(strassen):
        database.insert(adresse)


if __name__ == '__main__':
    import addressDb

    saveAllStrassen()
    database = addressDb.adressDb()
    saveAllAdressenFromStrassen(loadAllStrassen(), database)
