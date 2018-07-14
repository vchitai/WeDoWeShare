from flask import session, render_template, request, flash, abort, g, jsonify

from app import app, mongo
from models import jsonData


@app.route("/")
def home():
    if not session.get('logged_in'):
        return login_get()
    else:
        return render_template('home.html')

@app.route('/login')
def login_get():
    return render_template('login.html', css_file="login")

@app.route('/signup')
def register_get():
    return render_template('register.html', css_file="signup")

@app.route('/api/listOfUniversity')
def getListOfUniversity():
    return jsonify(jsonData['university'])

@app.route('/api/listOfFalcuty')
def getListOfFalcuty():
    return jsonify(jsonData['falculty'])

@app.route('/login', methods=['POST'])
def login_post():
    password =  request.form['password']
    username =  request.form['username']
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        abort(404)
    if user.check_password(password):
        session['logged_in'] = True
        g.user = user
    else:
        flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False

    return home()


@app.route("/register", methods=['POST'])
def register():
    password =  request.form['password']
    username =  request.form['username']
    admin = mongo.db.users.insert_one({"username": username, "password": password})
    return home()


@app.route("/tim-partner")
def tim_partner():
    nganh = request.args.get('nganh')
    if nganh is None:
        return render_template("major.html")
    truong = request.args.get('truong')
    if truong is None:
        return render_template("chon_truong.html")
    return render_template("suggest_tvv.html")
