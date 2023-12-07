from flask import Blueprint, jsonify, request
from DB_Connect import myDB as sqlcon
import mysql.connector

app = Blueprint('nady', __name__)

@app.route('/getallproducts', methods=['GET'])
def get_all_product():

    cursor = sqlcon.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    # Return the data as a JSON response
    return jsonify(data)


@app.route('/getproductinfo', methods=['GET'])
def get_product_info():
    id = request.args.get('id')
    cursor = sqlcon.cursor()
    query = f"SELECT * FROM product where id = {id} "
    cursor.execute(query)
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    # Return the data as a JSON response
    return jsonify(data)



@app.route("/ndy")
def hello_world():
    return "<h1 style='text-align: center;'>Welcome From Nady Side</h1>"

if __name__ == '__main__':
    app.run(debug=True)