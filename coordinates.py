import math
import pyproj
import requests

HOST = 'http://localhost:5000'

def getCoordinateFromBbox(bbox):
    return [(bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2]


def OSM_LongLat(utm32U):
    transformer = pyproj.Transformer.from_crs("epsg:5972", "epsg:4326")
    latlon = transformer.transform(utm32U[0], utm32U[1])
    return {'lon': latlon[1], 'lat': latlon[0]}


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


if __name__ == "__main__":
    import sys
    print(getCoordinate(sys.argv[1]))
