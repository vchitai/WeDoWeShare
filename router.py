import json

import simplejson as simplejson
from flask import session, render_template, request, flash, abort, g

from app import app
from models import User, db


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

@app.route('/login', methods=['POST'])
def login_post():
    password =  request.form['password']
    username =  request.form['username']
    user = User.query.filter_by(username=username).first()
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
    admin = User(username, password)
    db.session.add(admin)
    db.session.commit()
    return home()


@app.route("/tim-partner")
def tim_partner():
    with open("summary.json", "r") as f:
        x = simplejson.loads(f.read())
        print x
    nganh = request.args.get('nganh')
    if nganh is None:
        return render_template("chon_nganh.html")
    truong = request.args.get('truong')
    if truong is None:
        return render_template("chon_truong.html")
    return render_template("suggest_tvv.html")
