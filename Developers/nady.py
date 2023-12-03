from flask import Blueprint, jsonify
from flaskext.mysql import MySQL


app = Blueprint('nady', __name__)



@app.route("/nady")
def hello_world():
    return "<h1 style='text-align: center;'>Welcome From Nady Side</h1>"