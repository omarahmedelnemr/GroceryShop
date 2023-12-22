from flask import Blueprint, jsonify, request
from DB_Connect import myDB as sqlcon

app = Blueprint('nady', __name__)

@app.route('/getallproducts', methods=['GET'])
def get_all_product():
    try:

        cursor = sqlcon.cursor()
        cursor.execute("SELECT * FROM product")
        data = cursor.fetchall()

        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify(data)
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
        status = 406


    cursor.close()
    return response,status


@app.route('/filterbyprice', methods=['GET'])
def fliter_by_price():
    try:
  
        min= request.args.get('min')
        max = request.args.get('max')
        cursor = sqlcon.cursor()
        query = f'SELECT * FROM product WHERE productPrice BETWEEN {min} AND {max};'

        cursor.execute(query)
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify(data)
    
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
        status = 406


    cursor.close()
    return response,status



@app.route('/confirm', methods=['POST'])
def confirm():
    try:
  
        userID= request.json.get('userID')
        orderDate= request.json.get('orderDate')
        delevaryDate= request.json.get('delevaryDate')
        status= request.json.get('status')
       
        cursor = sqlcon.cursor()
        query = f"""INSERT INTO `Order` (totalPrice, orderDate, delevaryDate, status, userID)
                    VALUES (
                        (SELECT Cart.totalPrice FROM Cart WHERE Cart.userID = {userID} ),
                        {orderDate}, {delevaryDate}, {status}, {userID}
                    ); """
        cursor.execute(query)
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify(data)
    
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
        status = 406


    cursor.close()
    return response,status



@app.route('/filterbybrand', methods=['GET'])
def fliter_by_brand():
    try:
  
        brand= request.args.get('brand')
        cursor = sqlcon.cursor()
        query = f'SELECT * FROM product INNER JOIN Brand ON product.brand = Brand.id WHERE Brand.name = {brand};'

        cursor.execute(query)
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify(data)
    
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
        status = 406


    cursor.close()
    return response,status



@app.route('/addproductcart', methods=['POST'])
def add_to_cart():
    try:
  
        id = request.json.get('id')
        prodID = request.json.get('prodID')
        cartID = request.json.get('cartID')
        quan = request.json.get('quan')

        cursor = sqlcon.cursor()
        query = f'INSERT INTO CartProduct (id, productID, cartID, quantity) VALUES ({id},{prodID},{cartID},{quan});'

        cursor.execute(query)
        sqlcon.commit()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify('inserted Sucssefully')
    
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
        status = 406


    cursor.close()
    return response,status



@app.route('/deletefromcart', methods=['DELETE'])
def delete_from_cart():
    try:
  
        id = request.json.get('id')
        prodID = request.json.get('prodID')
        cartID = request.json.get('cartID')
        quan = request.json.get('quan')

        cursor = sqlcon.cursor()
        query = f'delete from CartProduct where id = {id} and productID = {prodID} and cartID = {cartID} and quantity = {quan}; '

        cursor.execute(query)
        sqlcon.commit()

        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify('Deleted Sucssefully')
    
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
        status = 406
        return response,status


@app.route('/getproductinfo', methods=['GET'])
def get_product_info():
    try:
            
        id = request.args.get('id')
        cursor = sqlcon.cursor()
        query = f"SELECT * FROM product where id = {id} "
        cursor.execute(query)
        data = cursor.fetchall()
        # Close the database connection
        cursor.close()
        # Return the data as a JSON response
        return jsonify(data)
    
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
        status = 406
    cursor.close()
    return response,status    



@app.route("/ndy")
def hello_world():
    return "<h1 style='text-align: center;'>Welcome From Nady Side</h1>"

if __name__ == '__main__':
    app.run(debug=True)