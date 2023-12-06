from flask import Blueprint, jsonify
from DB_Connect import myDB


app = Blueprint('adham', __name__)

@app.route("/adham")
def hello_world():
    return "<h1 style='text-align: center;'>Welcome From Adham Side</h1>"

    