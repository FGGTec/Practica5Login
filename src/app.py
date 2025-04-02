from flask import Flask, render_template, redirect, request, url_for, flash
from config import config
from flask_mysqldb import MySQL
from models.ModelUsers import ModelUsers
from models.entities.users import User

app = Flask(__name__)
db = MySQL(app)

@app.route("/")
def index():
    return redirect("login")
"""  
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _user = request.form["username"]
        _pass = request.form["password"]
        print(_user)
        print(_pass)
        if _user == "admin" and _pass == "123":
            flash("Acceso otorgado...", "success")
            return redirect(url_for("home"))
        else:
            flash("Acceso rechazado...", "danger")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")
"""
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['username'], request.form['password'],0)
        logged_user = ModelUsers.login(db, user)
        if logged_user != None:
            if logged_user.usertype == 1:
                flash("Acceso a administrador otorgado...", "warning")
                return redirect(url_for("admin", username=logged_user.username))
            else:
                flash("Acceso a usuario otorgado...", "success")
                return redirect(url_for("home", username=logged_user.username))
        else:
            flash("Acceso a usuario rechazado...", "danger")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")
  
@app.route("/home")
def home():
    username = request.args.get("username", "Invitado")
    return (render_template("home.html", username=username))

@app.route("/admin")
def admin():
    username = request.args.get("username", "Invitado")
    return (render_template("admin.html", username=username))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()