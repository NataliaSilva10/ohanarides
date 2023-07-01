from flask_app import app
from flask import render_template, redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.ride import Ride
# from flask_app.models.message import message
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard/")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    user_data = {
        "user_id" : session["user_id"]
    }
    user = User.get_by_id(user_data)
    rides = Ride.get_all()
    return render_template("dashboard.html",user=user,rides=rides)

@app.route("/register/",methods=["POST"])
def register():
    if not User.validate(request.form):
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        session["confirm_password"] = request.form["confirm_password"]
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect("/dashboard/")

@app.route("/login/",methods=["POST"])
def login():
    user = User.get_by_email(request.form)
    if not user or not bcrypt.check_password_hash(user.password,request.form["password"]):
        flash("Invalid email/password","login")
        return redirect("/")
    session.clear()
    session["user_id"] = user.id
    return redirect("/dashboard/")

@app.route("/logout/")
def logout():
    session.clear()
    return redirect("/")
