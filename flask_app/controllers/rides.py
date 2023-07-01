from wsgiref import validate
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.ride import Ride
from flask_app.models.message import Message

def user():
    user_data = { "user_id" : session["user_id"] }
    return User.get_by_id(user_data)

def ride(ride_id):
    ride_data = { "ride_id" : ride_id }
    return Ride.get_by_id(ride_data)

def validation_failed(data):
        session["destination"] = data["destination"]
        session["pick_up_location"] = data["pick_up_location"]
        session["date"] = data["date"]
        session["details"] = data["details"]

def validation_succeeded(data):
    if "destination" in session:
        session.pop("destination")
    if "pick_up_location" in session:
        session.pop("pick_up_location")
    if "date" in session:
        session.pop("date")
    if "details" in session:
        session.pop("details")
    new_data = {
        "destination" : data["destination"],
        "pick_up_location" : data["pick_up_location"],
        "details" : data["details"],
        "date" : data["date"],
        "rider_id" : session["user_id"],   
    }
    if "ride_id" in data:
        new_data["ride_id"] = data["ride_id"]
    return new_data

@app.route("/rides_new/")
def rides_new():
    if "user_id" not in session:
        return redirect("/")
    return render_template("rides_new.html",user=user())

@app.route("/rides_one/<int:ride_id>/")
def rides_one(ride_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "ride_id" : ride_id
    }
    messages = Message.get_messages(data)
    return render_template("rides_one.html",user=user(),ride=ride(ride_id),messages=messages)

@app.route("/rides_edit/<int:ride_id>/")
def ride_edit(ride_id):
    if "user_id" not in session:
        return redirect("/")
    return render_template("rides_edit.html",user=user(),ride=ride(ride_id))

@app.route("/rides_add/",methods=["POST"])
def rides_add():
    if "user_id" not in session:
        return redirect("/")
    if not Ride.validate(request.form):
        validation_failed(request.form)
        return redirect("/rides_new/")
    data = validation_succeeded(request.form)
    Ride.save(data)
    return redirect("/dashboard/")

@app.route("/rides_delete/<int:ride_id>/")
def rides_delete(ride_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "ride_id" : ride_id
    }
    Ride.delete(data)
    return redirect("/dashboard/")

@app.route("/rides_update/<int:ride_id>",methods=["POST"])
def rides_update(ride_id):
    if "user_id" not in session:
        return redirect("/")
    if not Ride.validate(request.form):
        validation_failed(request.form)
        return redirect(f"/rides_edit/{ride_id}")
    data = validation_succeeded(request.form)
    Ride.update(data)
    return redirect(f"/rides_one/{ride_id}")

@app.route("/update_driver/<int:ride_id>/<driver_id>/")
def update_driver(ride_id,driver_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "ride_id" : ride_id,
        "driver_id" : None if driver_id == 'None' else driver_id,
    }
    Ride.update_driver(data)
    return redirect("/dashboard/")






