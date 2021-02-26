#!/usr/bin/env python3

"""
import schulen

naechste = schulen.next("Philosophenweg 28")

print(f'Die nächste Grundschule ist die "{naechste["grundschulen"]["name"]}" mit einem Fußweg von {naechste["grundschulen"]["distance"]:.2f}km')
print(f'Die nächste Gesamtschule ist die "{naechste["gesamtschulen"]["name"]}" mit einem Fußweg von {naechste["gesamtschulen"]["distance"]:.2f}km')
print(f'Die nächste Schule ist die {naechste["insgesamt"]["name"]}, eine {naechste["insgesamt"]["typ"]} mit einem Fußweg von {naechste["insgesamt"]["distance"]:.2f}km')
"""

# Import the python libraries
from pymongo import MongoClient
from pprint import pprint

# Choose the appropriate client
client = MongoClient()

# Connect to db
db = client.test
employee = db.employee

# Use the condition to choose the record
# and use the delete method
db.employee.delete_one({"Age": '42'})

Queryresult = employee.find_one({'Age': '42'})

pprint(Queryresult)
