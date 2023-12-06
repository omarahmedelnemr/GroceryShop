from flask import Flask
import mysql.connector


from Developers.adham import app as adham
from Developers.nady import app as nady
from Developers.nemr import app as nemr
app = Flask(__name__)


# Register blueprints
app.register_blueprint(adham, url_prefix='/')
app.register_blueprint(nady, url_prefix='/')
app.register_blueprint(nemr, url_prefix='/')

@app.route("/")
def hello_world():
    return "<h1 style='text-align: center;'>Hello From Main Side</h1>"



# MySQL configuration
myDB = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'myownsql',
    database = 'GroceryShop'    
)