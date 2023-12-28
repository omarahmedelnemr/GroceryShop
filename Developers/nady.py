from flask import Blueprint, jsonify, request
from DB_Connect import myDB as sqlcon
from datetime import datetime,timedelta

app = Blueprint('nady', __name__)

# Get Products List
@app.route('/getallproducts', methods=['GET'])
def get_all_product():
    # Check if the Database Lost The Connection
    if not (sqlcon.is_connected()):
        sqlcon.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:

        cursor = sqlcon.cursor(dictionary=True)
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
                FROM product INNER JOIN Brand ON product.brand = Brand.id;"""
        cursor.execute(query)
        data = cursor.fetchall()

        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify({"success": True, "data":data})
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406


    cursor.close()
    return response,status

# Get Product Filtered By Price
@app.route('/filterbyprice', methods=['GET'])
def fliter_by_price():
    # Check if the Database Lost The Connection
    if not (sqlcon.is_connected()):
        sqlcon.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
  
        min= request.args.get('min')
        max = request.args.get('max')
        if min == None or max == None:
            return {"success": False,"message":"Missing Parameter"},406
        cursor = sqlcon.cursor(dictionary=True)
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
                FROM product INNER JOIN Brand ON product.brand = Brand.id
                WHERE product.productPrice BETWEEN {min} AND {max};
                """
        cursor.execute(query)
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify({"success": True, "data":data})
    
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406


    cursor.close()
    return response,status

# Get Product Filtered By Brand Name
@app.route('/filterbybrand', methods=['GET'])
def fliter_by_brand():
    # Check if the Database Lost The Connection
    if not (sqlcon.is_connected()):
        sqlcon.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
  
        brand= request.args.get('brand')
        if brand == None:
            return {"success": False,"message":"Missing Parameter"},406
        cursor = sqlcon.cursor(dictionary=True)
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
                FROM product INNER JOIN Brand ON product.brand = Brand.id
                WHERE Brand.name = "{brand}";
                """
        cursor.execute(query)
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify({"success": True, "data":data})
    
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406


    cursor.close()
    return response,status

# Get a Spicific Product Info 
@app.route('/getproductinfo', methods=['GET'])
def get_product_info():
    # Check if the Database Lost The Connection
    if not (sqlcon.is_connected()):
        sqlcon.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
            
        id = request.args.get('prodID')
        if id == None:
            return {"success": False,"message":"Missing Parameter"},406
        cursor = sqlcon.cursor(dictionary=True)
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
                FROM product INNER JOIN Brand ON product.brand = Brand.id
                where product.id = {id} ;
                """
        cursor.execute(query)
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify({"success": True, "data":data})
    
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406
    cursor.close()
    return response,status    

# add a Product to a Cart With Quantity
@app.route('/addToCart', methods=['POST'])
def add_to_cart():
    # Check if the Database Lost The Connection
    if not (sqlcon.is_connected()):
        sqlcon.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
  
        prodID = request.json.get('prodID')
        userID = request.json.get('email')
        quan = request.json.get('quan')
        if prodID == None or userID == None or quan ==None:
            return {"success": False,"message":"Missing Parameter"},406
        cursor = sqlcon.cursor(dictionary=True)

        # Get Cart ID
        cursor.execute(f"SELECT id FROM Cart WHERE userID= '{userID}'")
        cartID = cursor.fetchone()['id']

        # Check if it is Already in The Cart
        cursor.execute(f"SELECT * from CartProduct WHERE productID = {prodID} AND cartID = {cartID}")
        prodCart = cursor.fetchone()
        if prodCart == None:
            
            # Insert Into The Table
            query = f'INSERT INTO CartProduct (productID, cartID, quantity) VALUES ({prodID},"{cartID}",{quan});'
            cursor.execute(query)
            sqlcon.commit()
        else:
            
            # Update Quantity Value
            query = f'UPDATE CartProduct SET quantity = quantity+{quan} WHERE cartID={cartID} and productID={prodID}'
            cursor.execute(query)
            sqlcon.commit()
        
        # Calcutale Added Total Price
        query = f"SELECT * FROM product WHERE id ={prodID}"
        cursor.execute(query)
        productInfo = cursor.fetchone()
        totalPrice = productInfo['productPrice']*quan - (productInfo['productPrice']*quan  * productInfo['discount'])

        # Update Cart Total Price
        query = f'UPDATE Cart SET totalPrice = totalPrice+{totalPrice} WHERE id={cartID}'
        cursor.execute(query)
        sqlcon.commit()

        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify({"success": True, "message":'inserted Sucssefully'})
    
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406


    cursor.close()
    return response,status

# Remove a Product  Quantity From Cart
@app.route('/removefromcart', methods=['DELETE'])
def delete_from_cart():
    # Check if the Database Lost The Connection
    if not (sqlcon.is_connected()):
        sqlcon.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
  
        prodID = request.json.get('prodID')
        userID = request.json.get('email')
        quan = request.json.get('quan')
        if prodID == None or userID == None or quan == None:
            return {"success": False,"message":"Missing Parameter"},406
        cursor = sqlcon.cursor(dictionary=True)
        
        # Get Cart ID
        cursor.execute(f"SELECT id FROM Cart WHERE userID= '{userID}'")
        cartID = cursor.fetchone()['id']
        
        # Check if it is Already in The Cart
        cursor.execute(f"SELECT * from CartProduct WHERE productID = {prodID} AND cartID = {cartID}")
        prodCart = cursor.fetchone()
        if prodCart == None:
            cursor.close()    
            return {"success": False,"message":"The Product is Not in The Cart"},406

        else:
            # Get Product Info
            query = f"SELECT * FROM product WHERE id ={prodID}"
            cursor.execute(query)
            productInfo = cursor.fetchone()

            if (prodCart["quantity"] - quan )<=0:
                # Delete the Row
                query = f"DELETE FROM CartProduct WHERE cartID={cartID} and productID={prodID};"
                cursor.execute(query)
                sqlcon.commit()

                # Calcutale Added Total Price
                totalPrice = productInfo['productPrice']*prodCart["quantity"] - (productInfo['productPrice']*prodCart["quantity"]  * productInfo['discount'])

                # Update Cart Total Price
                query = f'UPDATE Cart SET totalPrice = totalPrice-{totalPrice} WHERE id={cartID}'
                cursor.execute(query)
                sqlcon.commit()
            else:

                # Update Quantity Value
                query = f'UPDATE CartProduct SET quantity = quantity-{quan} WHERE cartID={cartID} and productID={prodID}'
                cursor.execute(query)
                sqlcon.commit()
        
                # Calcutale Added Total Price
                query = f"SELECT * FROM product WHERE id ={prodID}"
                cursor.execute(query)
                productInfo = cursor.fetchone()
                totalPrice = productInfo['productPrice']*quan - (productInfo['productPrice']*quan  * productInfo['discount'])

                # Update Cart Total Price
                query = f'UPDATE Cart SET totalPrice = totalPrice-{totalPrice} WHERE id={cartID}'
                cursor.execute(query)
                sqlcon.commit()


        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify({"success": True, "message":'Deleted Sucssefully'})
    
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406
        return response,status

# Transfar all Products From CartProducts To OrderProducts
@app.route('/confirm', methods=['POST'])
def confirm():
    # Check if the Database Lost The Connection
    if not (sqlcon.is_connected()):
        sqlcon.reconnect()
        print("DB Connection Was Lost, But Restored")
    try:
  
        userID = request.json.get('email')
        userPayment = request.json.get('payemntMethod')
        if userID ==None:
            return {"success": False,"message":"Missing Parameter"},406
        orderDate = str(datetime.now()).split(".")[0]
        delevaryDate = datetime.now() + timedelta(days=8)
        cursor = sqlcon.cursor(dictionary=True)
        query = f"""INSERT INTO `Order` (totalPrice, orderDate, delevaryDate, status, userID)
            VALUES (
                (SELECT Cart.totalPrice FROM Cart WHERE Cart.userID = '{userID}'),
                '{orderDate}', '{delevaryDate}', 'ordered', '{userID}'
            ); """

        cursor.execute(query)
        sqlcon.commit()

        # Get Order ID
        cursor.execute(f"SELECT id FROM `Order` WHERE userID='{userID}' AND orderDate='{orderDate}'")
        orderID = cursor.fetchone()['id']

        # Transfar all Products From CartProducts To OrderProducts
        query = f"""
        INSERT INTO orderProducts VALUES (
            {orderID},
            (SELECT cp.productID FROM CartProduct as cp
                inner JOIN Cart as c ON c.id = cp.cartID
                WHERE c.userID = 'Alice@gmail.com'),
            (SELECT cp.quantity FROM CartProduct as cp
                inner JOIN Cart as c ON c.id = cp.cartID
                WHERE c.userID = 'Alice@gmail.com')
        )
        """
        cursor.execute(query)
        sqlcon.commit()

        # Delete All Products in the Cart
        # Get Cart ID
        cursor.execute(f"SELECT id FROM Cart WHERE userID= '{userID}'")
        cartID = cursor.fetchone()['id']

        query = f"DELETE FROM CartProduct WHERE cartID={cartID}"
        cursor.execute(query)
        sqlcon.commit()

        # Empty The Cart
        query = f"UPDATE Cart SET totalPrice=0 WHERE id={cartID}"
        cursor.execute(query)
        sqlcon.commit()

        # Close the Connection
        cursor.close()

        # Return the data as a JSON response
        return jsonify({'success': True})
    
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406


    cursor.close()
    return response,status

