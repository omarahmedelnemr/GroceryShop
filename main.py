from flask import Flask


from Developers.adham import app as adham
from Developers.nady import app as nady
from Developers.nemr import app as nemr
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# Register blueprints
app.register_blueprint(adham, url_prefix='/')

app.register_blueprint(nady, url_prefix='/')

app.register_blueprint(nemr, url_prefix='/')

@app.route("/")
def hello_world():
    return "<h1 style='text-align: center;'>Hello From Main Side</h1>"



if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)