from flask import Flask, jsonify, request
import mysql.connector

# app = Blueprint('adham', __name__)
# Tempraty for Error Handle
# MySQL configuration
app = Flask( __name__)
myDB = mysql.connector.connect(
    host = 'mysql-156876-0.cloudclusters.net',
    port = 10026,
    user = 'admin',
    password = '7TE9ESeh',
    database = 'GroceryShop'    
)


# Endpoint to search products by keyword
@app.route('/getBySearch', methods=['GET'])
def get_by_search():
    try:
        keyword = request.args.get('keyword', '')

       
        cursor = myDB.cursor(dictionary=True)

       
        query = f"SELECT * FROM Product WHERE productName LIKE '%{keyword}%'"
        cursor.execute(query)
        products = cursor.fetchall()

        # Convert the query result to a list of dictionaries for JSON serialization
        product_list = [
            {
                'id': product['id'],
                'brand': product['brand'],
                'productImage': product['productImage'],
                'productName': product['productName'],
                'productPrice': float(product['productPrice']),
                'quantity': product['quantity'],
                'nationality': product['nationality'],
                'discount': float(product['discount']),
            }
            for product in products
        ]

        cursor.close()

        return jsonify({'success': True, 'products': product_list})

    except Exception as e:
        print('Error executing search query:', str(e))
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500
    
    # Endpoint to filter products by nationality
@app.route('/filterByNationality', methods=['GET'])
def filter_by_nationality():
    try:
        nationality = request.args.get('Nationality', '')

        # Create a cursor object to interact with the database
        cursor = myDB.cursor(dictionary=True)

       
        query = f"SELECT * FROM Product WHERE nationality = '{nationality}'"
        cursor.execute(query)
        products = cursor.fetchall()

        # Convert the query result to a list of dictionaries for JSON serialization
        product_list = [
            {
                'id': product['id'],
                'brand': product['brand'],
                'productImage': product['productImage'],
                'productName': product['productName'],
                'productPrice': float(product['productPrice']),
                'quantity': product['quantity'],
                'nationality': product['nationality'],
                'discount': float(product['discount']),
            }
            for product in products
        ]

        cursor.close()

        return jsonify({'success': True, 'products': product_list})

    except Exception as e:
        print('Error executing nationality filter query:', str(e))
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500


