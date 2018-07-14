from flask import Flask, redirect, request, abort, render_template

app = Flask(__name__,
            static_folder='./static',
            static_url_path="")


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/tim-partner")
def tim_partner():
    nganh = request.args.get('nganh')
    if nganh is None:
        return render_template("chon_nganh.html")
    truong = request.args.get('truong')
    if truong is None:
        return render_template("chon-truong.html")
    render_template("suggest_tvv.html")


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()
