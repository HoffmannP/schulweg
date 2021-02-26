import pymongo

class addressDb:
    def __init__(self):
        client = pymongo.MongoClient()
        db = client.Schulwege
        self.addresses = db.addresses
        self.addresses.create_index([('name', pymongo.ASCENDING)], unique=True)
        self.addresses.create_index([('name', pymongo.TEXT)])

    def insert(self, adresse):
        try:
            self.addresses.insert_one(adresse)
        except pymongo.errors.DuplicateKeyError as e:
            print(e.details["errmsg"])

    def update(self, name, adresse):
        self.addresses.update_one(
            { 'name': name },
            adresse)

    def set_naechste(self, adresse, naechste):
        self.addresses.update_one(
            { 'name': adresse['name'] },
            { '$set': { 'naechste': naechste }})

    def get_alle(self):
        return self.addresses.find()

    def get_ohne_naechste(self):
        return self.addresses.find({ 'naechste': { '$exists': False }})
