from flask import Blueprint, request, jsonify
import jwt
from middleware.sendMail import generate_random_code,send_email
from DB_Connect import myDB
from datetime import datetime

jwtSecret = 'GroceryShop' 

app = Blueprint('nemr', __name__,url_prefix='/')

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    cursor = myDB.cursor(dictionary=True)

    try: 

        email = request.json.get('email')
        password = request.json.get('password')

        # Check Parameter Exictence
        if (email == None or password == None):
            cursor.close()
            return {"success": False,"message":"Missing Parameter"},406

        # Check if the user exists in the Users table
        query = f"SELECT * FROM User WHERE email = '{email}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        # Check if the User Exist
        if user != None:
            
            # Generate JWT token
            payload = {
                'email': user['email']
            }
            token = jwt.encode(payload, jwtSecret, algorithm='HS256')
            user["token"] = token            
            response =  jsonify({"success": True,"data":user})
            status = 200
        else:
            response =  jsonify({"success": False,'message': 'Wrong Email or Password'})
            status = 404
    except Exception as e:
            response = jsonify({"success": False,'message': f'Somthing Went Wrong: {str(e)}'})
            status = 406

    cursor.close()

    return response,status

# Endpoint for user signup
@app.route('/signup', methods=['POST'])
def signup():
    try: 
        email = request.json.get('email')
        name = request.json.get('name')
        phonenumber = request.json.get('phoneNumber')
        password = request.json.get('password')
        birthDate = request.json.get('birthDate')
        address = request.json.get('address')

        # Check Parameter Existence
        if (
            email          == None 
            or password    == None
            or name        == None
            or phonenumber == None
            or birthDate   == None
            or address     == None
            ):
            return {"success": False,"message":"Missing Parameter"},406

        # Connect to the MySQL database
        cursor = myDB.cursor(dictionary=True)

        # check if User Exist 
        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        if cursor.fetchall() !=[]:
             cursor.close()
             return {"success": False,"message":"Email Are Already in Use"},406

        # Insert a new user into the Users table
        query = f"""INSERT INTO User (email,password,name,phoneNumber,birthDate,address)VALUES ( 
        '{email}',
        '{password}', 
        '{name}', 
        '{phonenumber}', 
        '{datetime.strptime(birthDate, "%Y-%m-%d").date()}',
        '{address}'
        )
        """
        cursor.execute(query)
        myDB.commit()

        # Create a Cart For the User
        query = f"INSERT INTO Cart (id,totalPrice,userID) VALUES (default,0,'{email}')"
        cursor.execute(query)
        myDB.commit()

        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        newUser = cursor.fetchone()
        

        # Close the database connection

        # Generate JWT token
        payload = {
            'email':email,    
        }

        token = jwt.encode(payload, jwtSecret, algorithm='HS256')

        newUser['token'] = token
        # Return the token in the response
        response =  jsonify({"success": True,"message":"Done",'data': newUser})
        status = 200
    except Exception as e:
        response =  jsonify({"success": False,'message': f"Somthing Went Wrong: {str(e)}"})
        status = 406


    cursor.close()
    return response,status

# Sending OTP for Verfication 
@app.route("/send-otp",methods=["POST"])
def send_OTP():
    try:
        email = request.json.get("email")
        
        # Check Parameter Exictence
        if (email == None):
            return {"success": False, "message":"Missing Parameter"},406
        
        otp = generate_random_code()

        # DB
        cursor = myDB.cursor(dictionary=True)

        # Delete Eny Old OTPs
        query = f"DELETE FROM otp where email = '{email}';"
        cursor.execute(query)

        #  Save in DB
        query = f"INSERT INTO otp(email, otp) VALUES ('{email}','{otp}');"
        cursor.execute(query)
        myDB.commit()
        print("OTP is Saved")

        #  Send the OTP in Message
        send_email(email,"Grocery Shop Verfication Code",f"Your OTP Code is :{otp}")

        cursor.close()
        return {"success": True, "message":"Email is Sent"}, 200
    except Exception as e:
        return {"success": False, "message":f"Somthing Went Wrong: {str(e)}"},406

# Validating OTP for Verfication 
@app.route("/check-otp",methods=["POST"])
def check_OTP():
    try:
        email = request.json.get("email")
        otp_sent = request.json.get("otp")
        if email == None or otp_sent ==None:
            return {"success": False, "message":"Missing Parameter"},406
        # DB
        cursor = myDB.cursor(dictionary=True)

        # Get The Users OTP
        query = f"SELECT otp FROM otp where email = '{email}';"
        cursor.execute(query)
        otp_saved = cursor.fetchone()[0]
        if (int(otp_sent) != int(otp_saved)):
            return {"success": False, "message":"Wrong Code"},404
        
        #  Delete From DB
        query = f"DELETE FROM otp where email = '{email}';"
        cursor.execute(query)
        myDB.commit()
        print("OTP is DELETED")

        # Set a Security Token For Private Operations
        token = jwt.encode({"status":"secure"},jwtSecret,algorithm="HS256")

        return {"success": True,"token":token},200
    except Exception as e:
        return {"success": False, "message":f"Somthing Went Wrong: {str(e)}"},406

# Change Password Using token and New Passwords
@app.route('/forget-password',methods= ['POST'])
def forget():
    cursor = myDB.cursor(dictionary=True)
    try:

        email = request.json.get("email")
        token = request.json.get("token")
        password = request.json.get("newPassword")
        
        # Check Parameter Exictence
        if (email == None or password == None or token == None):
            return {"success": False, "message":"Missing Parameter"},406
        
        # Check the Token
        try:
            verf = jwt.decode(token,jwtSecret,algorithms="HS256")
        except Exception as e:
            return {"message":"The Token is Wrong, Not Authorized"},401
        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{password}' WHERE email = '{email}'"
        print(query)
        cursor.execute(query)
        myDB.commit()
        
        response =  jsonify({"success": True, "message":"Password has Been Reset"})
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing Went Wrong: {str(e)}"})

    cursor.close()
    print(response)
    return response

# Change Password Using old and New Passwords
@app.route('/change-password',methods= ['POST'])
def change():
    try:
        cursor = myDB.cursor(dictionary=True)

        email = request.json.get("email")
        oldpassword = request.json.get("oldpassword")
        newpassword = request.json.get("newPassword")

        # Check Parameter Exictence
        if (email == None or oldpassword == None or newpassword == None):
            return {"success": False, "message":"Missing Parameter"},406

        # Check Password
        query = f"SELECT password FROM User WHERE email = '{email}'"
        cursor.execute(query)
        user_password = cursor.fetchone()[0]
        print(f"New {newpassword} Old: {oldpassword}, real: {user_password}")
        if(user_password != oldpassword):
            return {"success": False,"message":"Wrong Password"},406
        
        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{newpassword}' WHERE email = '{email}'"
        cursor.execute(query)
        myDB.commit()
        
        cursor.close()
        return jsonify({"success": True,"message":"Password Changed"}), 200
    except Exception as e:
        cursor.close()
        return jsonify({"success": False,'message': f"Somthing Went Wrong: {str(e)}"}), 406

# Get All Products in the Cart
@app.route('/cart-products', methods=['GET'])
def get_user_cart_products():
    try:
        user_id = request.args.get('email')

        if user_id == None:
            return jsonify({"success": False, "message":"Missing Parameter"}),406
        
        # Create a cursor object to interact with the database
        cursor = myDB.cursor(dictionary=True)

        # Perform a search for orders associated with the user
        query = f"SELECT * FROM `Cart` WHERE userID = '{user_id}'"
        cursor.execute(query)
        cart = cursor.fetchone()

        query = f"""
            SELECT 
                product.id,
                product.productName,
                product.productPrice,
                product.productImage,
                cp.quantity as orderedQuantity,
                product.calories,
                product.discount,
                Brand.name as brand,
                Brand.nationality 
            FROM CartProduct as cp 
                INNER JOIN product on cp.productID=product.id 
                INNER JOIN Brand on product.brand = Brand.id 
            WHERE cp.cartID={cart['id']};
        """
        cursor.execute(query)
        cart['products'] = cursor.fetchall()

        cursor.close()

        return jsonify({'success': True, 'data': cart})

    except Exception as e:
        print('Error executing get_user_orders query:', str(e))
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

# Get All Products That Has a Discount
@app.route('/discounts', methods=['GET'])
def get_all_discounts():
    try:

        # Create a cursor object to interact with the database
        cursor = myDB.cursor(dictionary=True)

        query = f"""
            SELECT product.id,
                product.productName,
                product.productPrice,
                product.productImage,
                product.calories,
                product.discount,
                Brand.name as brand,
                Brand.nationality
            FROM product
                INNER JOIN Brand on product.brand = Brand.id
            WHERE product.discount>0
            ORDER BY product.discount DESC;
        """
        cursor.execute(query)
        discount_list = cursor.fetchall()

        cursor.close()

        return jsonify({'success': True, 'data': discount_list})

    except Exception as e:
        print('Error executing get_user_orders query:', str(e))
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

# Get All Brands on the System
@app.route('/brands', methods=['GET'])
def get_all_brands():
    try:

        # Create a cursor object to interact with the database
        cursor = myDB.cursor(dictionary=True)

        query = f"""
            SELECT * From Brand
                
        """
        cursor.execute(query)
        discount_list = cursor.fetchall()

        cursor.close()

        return jsonify({'success': True, 'data': discount_list})

    except Exception as e:
        print('Error executing get_user_orders query:', str(e))
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

# Cancel an Order
@app.route('/order', methods=['DELETE'])
def cancelOrder():
    try:
  
        orderID = request.json.get('orderID')
        if orderID ==None:
            return {"success": False,"message":"Missing Parameter"},406
        cursor = myDB.cursor(dictionary=True)

        # Delete all Products in the Order
        query = f"DELETE FROM orderProducts WHERE `order`={orderID}"
        cursor.execute(query)
        myDB.commit()

        # Delete the Order Itself
        query = f"DELETE FROM `Order` WHERE id={orderID}"
        cursor.execute(query)
        myDB.commit()

        # Close the Connection
        cursor.close()

        # Return the data as a JSON response
        return jsonify({'success': True,"message":"Order Canceled Successfully"})
    
    except Exception as e:
        response =  jsonify({"success": False, 'message': f"Somthing went Wrong: {str(e)}"})
        status = 406


    cursor.close()
    return response,status

