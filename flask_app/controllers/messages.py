from flask_app import app
from flask import render_template,redirect,request,session,flash
# from flask_app.models.user import User
# from flask_app.models.ride import Ride
from flask_app.models.message import Message

@app.route("/post_message/<ride_id>/",methods=["POST"])
def post_message(ride_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "sender_id" : session["user_id"],
        "ride_id" : ride_id,
        "content" : request.form["content"],
    }
    if Message.validate(request.form):
        Message.save(data)
    return redirect(f"/rides_one/{ride_id}/")
    