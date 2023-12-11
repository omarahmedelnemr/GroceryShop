from flask import Flask


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


