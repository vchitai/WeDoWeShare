from flask import Flask
from models import db

# POSTGRES_USER = "ezyumsowiutaxj"
# POSTGRES_PW = "72e963c685c834b7fc84ac3589bc172164c81bc7d54b66a83251ba055e60a972"
# POSTGRES_URL = "ec2-54-163-235-56.compute-1.amazonaws.com"
# POSTGRES_DB = "dbhlkslcb9rjnf"
# POSTGRES_PORT = "5432"
POSTGRES_USER = "postgre"
POSTGRES_PW = "trunghieuhoang1997"
POSTGRES_URL = "192.168.33.156"
POSTGRES_DB = "KMSHackathon"
POSTGRES_PORT = "5432"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB,port=POSTGRES_PORT)

app = Flask(__name__,
            static_folder='./static',
            static_url_path="")
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
