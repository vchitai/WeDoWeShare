import simplejson
from werkzeug.security import generate_password_hash, \
     check_password_hash

with open("summary.json", "r") as f:
    jsonData = simplejson.loads(f.read())

class User():
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)