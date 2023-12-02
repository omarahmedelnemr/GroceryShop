from flask import Blueprint, jsonify

app = Blueprint('nemr', __name__)

@app.route("/nemr")
def hello_world():
    return "<h1 style='text-align: center;'>Welcome From Nemr Side</h1>"



@app.route("/login")
def hello_world():
    return "<h1 style='text-align: center;'>Welcome From login</h1>"