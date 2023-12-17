from flask import Blueprint, Flask, jsonify, request
import mysql.connector


app = Flask(__name__)

# MySQL configuration
myDB = mysql.connector.connect(
    host='mysql-158141-0.cloudclusters.net',
    port=10014,
    user='admin',
    password='oGFpwVr8',
    database='GroceryShop'
)

# Endpoint to search products by keyword
@app.route('/getBySearch', methods=['GET'])
def get_by_search():
    try:
        keyword = request.args.get('keyword')

        cursor = myDB.cursor(dictionary=True)



       

        query = f"SELECT * FROM product WHERE productName LIKE '%{keyword}%'"
        cursor.execute(query)
        products = cursor.fetchall()

        product_list = [
            {
                'id': product['id'],
                'productImage': product['productImage'],
                'productName': product['productName'],
                'productPrice': float(product['productPrice']),
                'quantity': product['quantity'],
                'nationality': product['nationality'],
                'brand': product['brand'],
                'discount': float(product['discount']),
                'calories': product['calories']
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

        cursor = myDB.cursor(dictionary=True)

        query = f"SELECT * FROM product WHERE nationality = '{nationality}'"
        cursor.execute(query)
        products = cursor.fetchall()

        product_list = [
            {
                'id': product['id'],
                'productImage': product['productImage'],
                'productName': product['productName'],
                'productPrice': float(product['productPrice']),
                'quantity': product['quantity'],
                'nationality': product['nationality'],
                'brand': product['brand'],
                'discount': float(product['discount']),
                'calories': product['calories']
            }
            for product in products
        ]

        cursor.close()

        return jsonify({'success': True, 'products': product_list})

    except Exception as e:
        print('Error executing nationality filter query:', str(e))
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500

# Endpoint to get payment methods for a user
@app.route('/getPaymentMethods', methods=['GET'])
def get_payment_methods():
    try:
        user_id = request.args.get('userId', '')

        cursor = myDB.cursor(dictionary=True)

        query = f"SELECT * FROM PayementMethods WHERE userID = '{user_id}'"
        cursor.execute(query)
        payment_methods = cursor.fetchall()

        payment_methods_list = [
            {
                'id': method['id'],
                'userID': method['userID'],-
                'cardNumber': method['cardNumber'],
                'cvv': method['cvv'],
                'cardHolderName': method['cardHolderName'],
            }
            for method in payment_methods
        ]

        cursor.close()

        return jsonify({'success': True, 'paymentMethods': payment_methods_list})

    except Exception as e:
        print('Error executing getPaymentMethods query:', str(e))
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500
    
 # Endpoint to add payment methods
@app.route('/addPaymentMethods', methods=['POST'])
def add_payment_methods():
    try:
        data = request.json

        user_id = data.get('userID')
        card_number = data.get('cardNumber')
        cvv = data.get('cvv')
        card_holder_name = data.get('cardHolderName')

        cursor = myDB.cursor()
        # Corrected table name to 'PaymentMethods'
        query = "INSERT INTO PayementMethods (userID, cardNumber, cvv, cardHolderName) VALUES (%s, %s, %s, %s)"
        values = (user_id, card_number, cvv, card_holder_name)
        cursor.execute(query, values)
        myDB.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Payment method added successfully'})
    except Exception as e:
        print('Error adding payment method:', str(e))
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500


# Endpoint to remove payment methods
@app.route('/removePaymentMethods', methods=['DELETE'])
def remove_payment_methods():
    try:
        user_id = request.args.get('userId', '')
        payment_method_id = request.args.get('paymentMethodId', '')
        cursor = myDB.cursor()
        # Delete the specified payment method
        query = "DELETE FROM PayementMethods WHERE userID = %s AND id = %s"
        values = (user_id, payment_method_id)
        cursor.execute(query, values)
        myDB.commit()

        cursor.close()

        return jsonify({'success': True, 'message': 'Payment method removed'}), 500
    except Exception as e:
        # Handle the exception (you might want to log it or return an error response)
        return jsonify({'success': False, 'message': str(e)}), 500
    
# Endpoint to get user's orders
@app.route('/myOrder', methods=['GET'])
def get_user_orders():
    try:
        user_id = request.args.get('userId', '')

        # Create a cursor object to interact with the database
        cursor = myDB.cursor(dictionary=True)

        # Perform a search for orders associated with the user
        query = f"SELECT * FROM `Order` WHERE userID = '{user_id}'"
        cursor.execute(query)
        orders = cursor.fetchall()

        # Convert the query result to a list of dictionaries for JSON serialization
        orders_list = [
            {
                'id': order['id'],
                'totalPrice': float(order['totalPrice']),
                'orderDate': order['orderDate'].isoformat(),
                'deliveryDate': order['delevaryDate'].isoformat(),
                'status': order['status'],
                'userID': order['userID'],
            }
            for order in orders
        ]

        cursor.close()

        return jsonify({'success': True, 'orders': orders_list})

    except Exception as e:
        print('Error executing get_user_orders query:', str(e))
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500
