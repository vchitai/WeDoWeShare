import simplejson
from werkzeug.security import generate_password_hash, \
     check_password_hash

from app import mongo

with open("summary.json", "r") as f:
    jsonData = simplejson.loads(f.read())

class User():
    def __init__(self, dicts):
        self.__dict__ = dicts

    def hash_password(self, password):
        self.__dict__['password'] = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__dict__['password'], password)

    def commit(self):
        mongo.db.users.insert_one(self.__dict__)