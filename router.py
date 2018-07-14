from flask import session, render_template, request, flash

from app import app


@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"


@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/tim-partner")
def tim_partner():
    nganh = request.args.get('nganh')
    if nganh is None:
        return render_template("chon_nganh.html")
    truong = request.args.get('truong')
    if truong is None:
        return render_template("chon-truong.html")
    render_template("suggest_tvv.html")
