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

def getUniversityIndex(university):
    return jsonData["stupid-list-2"].index(university)

def getMajorIndex(major):
    return jsonData["stupid-list"].index(major)



def convertResultToListOfList(mes):
    mes = mes.replace('\n','')
    mes = mes.replace('u','')
    mes = mes.split(']')
    res = []
    for i in mes:
        tmp = i.replace('[','').split(' ')
        tmp = filter(lambda a: a != '', tmp)
        tmp = tmp[1:]
        for i in range(len(tmp)):
            tmp[i] = int(str(tmp[i]))
        if (len(tmp)!=0):
            res.append(tmp)
    return res

with open("summary.json", "r") as f:
    jsonData = simplejson.loads(f.read())

class User():
    def __init__(self, dicts):
        self.__dict__ = dict(dicts)
        for i in self.__dict__:
            if isinstance(self.__dict__, list):
                self.__dict__[i] = self.__dict__[i][0]



    def hash_password(self, password):
        self.__dict__['password'] = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__dict__['password'], password)

    def commit(self):
        mongo.db.users.insert_one(self.__dict__)