from flask import Flask, render_template, redirect, request, url_for, flash, abort
from config import config
from flask_mysqldb import MySQL
from models.ModelUsers import ModelUsers
from models.entities.users import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
# Verificar si el usuario está autenticado y es un administrador
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403) # Acceso prohibido
        return func(*args, **kwargs)
    return decorated_view

@app.route("/")
def index():
    return redirect("login")
'''@app.route("/login", methods=["GET", "POST"])
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
        return render_template("auth/login.html")'''
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['username'], request.form['password'],0)
        logged_user = ModelUsers.login(db, user)
        if logged_user != None:
            login_user(logged_user)

            if logged_user.usertype == 1:
                flash("Acceso a administrador otorgado...", "warning")
                #return redirect(url_for("admin", username=logged_user.username))
                return redirect(url_for("admin"))
            else:
                flash("Acceso a usuario otorgado...", "success")
                #return redirect(url_for("home", username=logged_user.username))
                return redirect(url_for("home"))
        else:
            flash("Acceso a usuario rechazado...", "danger")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

@app.route("/home")
@login_required
def home():
    '''username = request.args.get("username", "InvitadoH")
    return (render_template("home.html", username=username))'''
    return (render_template("home.html"))

@app.route("/admin")
@login_required
@admin_required
def admin():
    '''username = request.args.get("username", "InvitadoA")
    return (render_template("admin.html", username=username))'''
    return (render_template("admin.html"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()