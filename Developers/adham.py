from flask import Blueprint, jsonify, request
from DB_Connect import myDB


app = Blueprint('adham', __name__)

# search products by keyword
@app.route('/getBySearch', methods=['GET'])
def get_by_search():
    # Check if the Database Lost The Connection
    if not (myDB.is_connected()):
        myDB.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
        keyword = request.args.get('keyword')
        # Check Parameter Existence
        if keyword == None:
            return {"success": False, "message":"Missing Parameter"},406
        
        cursor = myDB.cursor(dictionary=True)
        query = f"""
                SELECT
                    product.id,
                    product.productName,
                    product.productPrice,
                    product.productImage,
                    product.quantity,
                    product.calories,
                    product.discount,
                    Brand.name as brand,
                    Brand.nationality 
                FROM product INNER JOIN Brand ON product.brand = Brand.id WHERE product.productName LIKE '%{keyword}%';"""
        cursor.execute(query)
        products = cursor.fetchall()

        #  Adding Orders Number and Last 24 Hours Orders
        for i in range(len(products)):
            query = f"SELECT COUNT(*) as c  FROM orderProducts WHERE product={products[i]['id']};"
            cursor.execute(query)
            products[i]["totalOrdersNumber"] = cursor.fetchone()['c']

            query = f"SELECT COUNT(*) as c FROM orderProducts inner join `Order` as ord on orderProducts.`order` = ord.id WHERE ord.orderDate>= NOW() - INTERVAL 24 HOUR and product={products[i]['id']};"
            cursor.execute(query)
            products[i]["lastDayOrders"] = cursor.fetchone()['c']

        cursor.close()
        return jsonify({'success': True, 'data': products})

    except Exception as e:
        print('Error executing search query:', str(e))
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

# filter products by nationality
@app.route('/filterByNationality', methods=['GET'])
def filter_by_nationality():
    # Check if the Database Lost The Connection
    if not (myDB.is_connected()):
        myDB.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
        nationality = request.args.get('nationality')
        if nationality == None:
            return {"success": False, "message":"Missing Parameter"},406
        cursor = myDB.cursor(dictionary=True)

        query = f"""
                SELECT
                    product.id,
                    product.productName,
                    product.productPrice,
                    product.productImage,
                    product.quantity,
                    product.calories,
                    product.discount,
                    Brand.name as brand,
                    Brand.nationality 
                FROM product INNER JOIN Brand ON product.brand = Brand.id WHERE Brand.nationality = "{nationality}";"""
        cursor.execute(query)
        products = cursor.fetchall()

        #  Adding Orders Number and Last 24 Hours Orders
        for i in range(len(products)):
            query = f"SELECT COUNT(*) as c  FROM orderProducts WHERE product={products[i]['id']};"
            cursor.execute(query)
            products[i]["totalOrdersNumber"] = cursor.fetchone()['c']

            query = f"SELECT COUNT(*) as c FROM orderProducts inner join `Order` as ord on orderProducts.`order` = ord.id WHERE ord.orderDate>= NOW() - INTERVAL 24 HOUR and product={products[i]['id']};"
            cursor.execute(query)
            products[i]["lastDayOrders"] = cursor.fetchone()['c']

        cursor.close()

        return jsonify({'success': True, 'data': products})

    except Exception as e:
        print('Error executing nationality filter query:', str(e))
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

# get payment methods for a user
@app.route('/getPaymentMethods', methods=['GET'])
def get_payment_methods():
    # Check if the Database Lost The Connection
    if not (myDB.is_connected()):
        myDB.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
        user_id = request.args.get('userId')
        if user_id == None:
            return {"success": False, "message":"Missing Parameter"},406
        cursor = myDB.cursor(dictionary=True)

        query = f"SELECT * FROM PayementMethods WHERE userID = '{user_id}'"
        cursor.execute(query)
        payment_methods = cursor.fetchall()

        cursor.close()

        return jsonify({'success': True, 'data': payment_methods})

    except Exception as e:
        print('Error executing getPaymentMethods query:', str(e))
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

# add payment methods
@app.route('/addPaymentMethods', methods=['POST'])
def add_payment_methods():
    # Check if the Database Lost The Connection
    if not (myDB.is_connected()):
        myDB.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
        data = request.json

        user_id = data.get('userID')
        card_number = data.get('cardNumber')
        cvv = data.get('cvv')
        card_holder_name = data.get('cardHolderName')

        # Check Parameter Existence
        if (user_id == None
        or card_number == None
        or cvv == None
        or card_holder_name == None):
            return {"success": False, "message":"Missing Parameter"},406
 
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
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

# remove payment methods
@app.route('/removePaymentMethods', methods=['DELETE'])
def remove_payment_methods():
    # Check if the Database Lost The Connection
    if not (myDB.is_connected()):
        myDB.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
        user_id = request.args.get('userId')
        payment_method_id = request.args.get('paymentMethodId')
        if user_id == None or payment_method_id == None:
            return jsonify({"success": False, "message":"Missing Parameter"}),406
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
        return jsonify({'success': False, 'message': f"Internal Server Error: {str(e)}"}), 500
    
# get user's orders
@app.route('/myOrder', methods=['GET'])
def get_user_orders():
    # Check if the Database Lost The Connection
    if not (myDB.is_connected()):
        myDB.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
        user_id = request.args.get('email')

        if user_id == None:
            return jsonify({"success": False, "message":"Missing Parameter"}),406
        
        # Create a cursor object to interact with the database
        cursor = myDB.cursor(dictionary=True)

        # Perform a search for orders associated with the user
        query = f"SELECT * FROM `Order` WHERE userID = '{user_id}'"
        cursor.execute(query)
        orders = cursor.fetchall()

        for i in range(len(orders)):
            # Get Order Items
            query = f"""
                SELECT 
                    product.id,
                    product.productName,
                    product.productPrice,
                    product.productImage,
                    op.quantity as orderedQuantity,
                    product.calories,
                    product.discount,
                    Brand.name as brand,
                    Brand.nationality 
                FROM orderProducts as op 
                    INNER JOIN product on op.product=product.id 
                    INNER JOIN Brand on product.brand = Brand.id 
                WHERE `order`={orders[i]['id']};
            """
            cursor.execute(query)
            orders[i]['products'] = cursor.fetchall()

            #  Adding Orders Number and Last 24 Hours Orders
            for z in range(len(orders[i]['products'])):
                query = f"SELECT COUNT(*) as c  FROM orderProducts WHERE product={orders[i]['products'][z]['id']};"
                cursor.execute(query)
                orders[i]['products'][z]["totalOrdersNumber"] = cursor.fetchone()['c']

                query = f"SELECT COUNT(*) as c FROM orderProducts inner join `Order` as ord on orderProducts.`order` = ord.id WHERE ord.orderDate>= NOW() - INTERVAL 24 HOUR and product={orders[i]['products'][z]['id']};"
                cursor.execute(query)
                orders[i]['products'][z]["lastDayOrders"] = cursor.fetchone()['c']
                
        cursor.close()

        return jsonify({'success': True, 'data': orders})

    except Exception as e:
        print('Error executing get_user_orders query:', str(e))
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500
