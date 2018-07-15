import simplejson
from werkzeug.security import generate_password_hash, \
     check_password_hash
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
from app import mongo

with open("summary.json", "r") as f:
    jsonData = simplejson.loads(f.read())

class User():
    def __init__(self, dicts):
        self.__dict__ = dict(dicts)

    def hash_password(self, password):
        self.__dict__['password'] = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__dict__['password'], password)

    def commit(self):
        mongo.db.users.insert_one(self.__dict__)