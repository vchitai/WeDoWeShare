from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__,
            static_folder='./static',
            static_url_path="")
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MONGO_URI"] = "mongodb://192.168.33.156:27017/KMSHackathon"
mongo = PyMongo(app)