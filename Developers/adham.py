from flask import Blueprint, jsonify, request
from DB_Connect import myDB

app = Blueprint('adham', __name__)

# Endpoint to search products by keyword
@app.route('/getBySearch', methods=['GET'])
def get_by_search():
    try:
        keyword = request.args.get('keyword', '')

        # Create a cursor object to interact with the database
        cursor = myDB.cursor(dictionary=True)

        # Perform a case-insensitive search for products containing the keyword in productName
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