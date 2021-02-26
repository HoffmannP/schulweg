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
    return 'displaytext' in a and a['displaytext'].startswith(street)

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

    return [a['displaytext'] for a in response.json()["results"][1:] if isStrasse(a)]

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
    strassen = set()
    for letter in string.ascii_uppercase:
        strassen = strassen.union(getStrassen(letter))
    return [a[:-len(" (Strasse)")] for a in sorted(list(strassen))]

def saveAllStrassen(filename=DEFAULT_STRASSEN_SAVE):
    with open(filename, "w") as f:
        json.dump(getAllStrassen(), f)

def loadAllStrassen(filename=DEFAULT_STRASSEN_SAVE):
    with open(filename, "r") as f:
        strassen = json.load(f)
    return strassen

def getAllAdressenFromStrassen(strassen):
    adressen = []
    for strasse in strassen:
        print(f'{strasse}: ', end='')
        adressenInStrasse = getAdressenInStrasse(strasse)
        adressen.append(adressenInStrasse)
        print(f'{len(adressenInStrasse):3d}')
    return adressen

def saveAllAdressenFromStrassen(strassen, filename=DEFAULT_ADRESSEN_SAVE):
    with open(filename, "w") as f:
        json.dump(getAllAdressenFromStrassen(strassen), f)

def loadAllAdressen(filename=DEFAULT_ADRESSEN_SAVE):
    with open(filename, "r") as f:
        adressen = json.load(f)
    return adressen


if __name__ == '__main__':
    # saveAllStrassen()
    saveAllAdressenFromStrassen(loadAllStrassen())
