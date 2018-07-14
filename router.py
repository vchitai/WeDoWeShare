# -*- coding: utf-8 -*-

from flask import session, render_template, request, flash, abort, g, jsonify, url_for, redirect

from app import app, mongo
from models import jsonData, User


@app.route("/")
def home():
    if not session.get('logged_in'):
        return login_get()
    else:
        return render_template('home.html', css_file=["home"], page_title=u"Trang chủ")


@app.route('/login')
def login_get():
    return render_template('login.html', css_file=["login"], page_title=u"Đăng nhập")


@app.route('/signup')
def register_get():
    return render_template('register.html', css_file=["signup"], page_title=u"Đăng kí")


@app.route('/api/listOfUniversity')
def getListOfUniversity():
    return jsonify(jsonData['university'])


@app.route('/api/listOfFalcuty')
def getListOfFalcuty():
    return jsonify(jsonData['falculty'])


@app.route('/login', methods=['POST'])
def login_post():
    password = request.form['password']
    username = request.form['username']
    user = mongo.db.users.find_one({"username": username})
    user = User(user)
    if user is None:
        abort(404)
    print user.check_password(password)
    if user.check_password(password):
        session['logged_in'] = True
        g.user = user
        return home()
    else:
        flash(u'Mật khẩu sai')
        return login_get()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route("/register", methods=['POST'])
def register():
    password = request.form['password']
    username = request.form['username']
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        user = User({"username": username})
        user.hash_password(password)
        user.commit()
        return login_get()
    else:
        flash(u"Người dùng đã tồn tại")
        return register_get()

@app.route("/<nganh>")
def major_detail(nganh):
    return render_template("major-detail.html", page_title=u"Chi tiết ngành", css_file=["major-detail", "major"])

@app.route("/tim-partner")
def tim_partner():
    nganh = request.args.get('nganh')
    if nganh is None:
        return render_template("major.html", css_file=["major"], page_title=u"Chọn ngành")
    truong = request.args.get('truong')
    if truong is None:
        return render_template("chon_truong.html", page_title=u"Chọn trường")
    return render_template("suggest_tvv.html", page_title=u"Chọn tư vấn viên")
