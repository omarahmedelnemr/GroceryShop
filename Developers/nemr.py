from flask import Blueprint, request, jsonify
import jwt
from flask_cors import CORS
from middleware.labels import addLabels
from middleware.sendMail import generate_random_code,send_email
from main import myDB

jwtSecret = 'GroceryShop' 

app = Blueprint('nemr', __name__,url_prefix='/')
CORS(app)



# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    cursor = myDB.cursor()

    try: 

        email = request.json.get('email')
        password = request.json.get('password')

        # Check Parameter Exictence
        if (email == None or password == None):
            return {"message":"Missing Parameter"},406

        # Check if the user exists in the Users table
        query = f"SELECT * FROM User WHERE email = '{email}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        # Close the database connection
        if user != None:
            result = addLabels(user,cursor.description,0)
            
            # Generate JWT token
            payload = {
                'email': result['email']
            }
            print(payload)
            print("Flag 0")
            token = jwt.encode(payload, jwtSecret, algorithm='HS256')

            print("Flag 1")

            result["token"] = token
            response =  jsonify({'message': 'Done',"data":result})
            status = 200
        else:
            
            response =  jsonify({'message': 'Wrong Email or Password'})
            status = 404
    except:
            
            response = jsonify({'message': 'Somthing went Wrong'})
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

        # Check Parameter Exictence
        if (
            email          == None 
            or password    == None
            or name        == None
            or phonenumber == None
            or birthDate   == None
            or address     == None
            ):
            return {"message":"Missing Parameter"},406

        # Connect to the MySQL database
        cursor = myDB.cursor()

        # check if User Exist 
        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        if cursor.fetchall() !=[]:
             cursor.close()
             return {"message":"Email Are Already in Use"},406

        # Insert a new user into the Users table
        query = f"""INSERT INTO User (email,password,name,phoneNumber,birthDate,address)VALUES ( 
        '{email}',
        '{password}', 
        '{name}', 
        '{phonenumber}', 
        '{birthDate}',
        '{address}'
        )
        """
        cursor.execute(query)
        myDB.commit()

        query = f"SELECT * FROM User WHERE email = '{email}'"
        cursor.execute(query)
        newUser = cursor.fetchone()
        result = addLabels(newUser,cursor.description,0)

        # Close the database connection

        # Generate JWT token
        payload = {
            'email':email,    
        }

        token = jwt.encode(payload, jwtSecret, algorithm='HS256')

        result['token'] = token
        # Return the token in the response
        response =  jsonify({"message":"Done",'data': result})
        status =200
    except:
        response =  jsonify({'message': "Somthing went Wrong"})
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
            return {"message":"Missing Parameter"},406
        
        otp = generate_random_code()

        # DB
        cursor = myDB.cursor()

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
        return {"message":"Email is Sent"}, 200
    except:
        return {"message":"Somthing Went Wrong"},406

# Validating OTP for Verfication 
@app.route("/check-otp",methods=["POST"])
def check_OTP():
    try:
        email = request.json.get("email")
        otp_sent = request.json.get("otp")
        if email == None or otp_sent ==None:
            return {"message":"Missing Parameter"},406
        # DB
        cursor = myDB.cursor()

        # Get The Users OTP
        query = f"SELECT otp FROM otp where email = '{email}';"
        cursor.execute(query)
        otp_saved = cursor.fetchone()[0]
        if (int(otp_sent) != int(otp_saved)):
            return {"message":"Wrong Code"},404
        
        #  Delete From DB
        query = f"DELETE FROM otp where email = '{email}';"
        cursor.execute(query)
        myDB.commit()
        print("OTP is DELETED")

        # Set a Security Token For Private Operations
        token = jwt.encode({"status":"secure"},jwtSecret,algorithm="HS256")

        return {"message":"Email is Verified","token":token},200
    except:
        return {"message":"Somthing Went Wrong"},406

# Change Password Using token and New Passwords
@app.route('/forget-password',methods= ['POST'])
def forget():
    cursor = myDB.cursor()
    try:

        email = request.json.get("email")
        token = request.json.get("token")
        password = request.json.get("newPassword")
        
        # Check Parameter Exictence
        if (email == None or password == None or token == None):
            return {"message":"Missing Parameter"},406
        
        # Check the Token
        try:
            verf = jwt.decode(token,jwtSecret,algorithms="HS256")
        except:
            return {"message":"The Token is Wrong, Not Authorized"},401
        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{password}' WHERE email = '{email}'"
        print(query)
        cursor.execute(query)
        myDB.commit()
        
        response =  jsonify({"message":"Done"})
    except:
        response =  jsonify({'message': "Somthing went Wrong"})

    cursor.close()
    print(response)
    return response

# Change Password Using old and New Passwords
@app.route('/change-password',methods= ['POST'])
def change():
    try:
        cursor = myDB.cursor()

        email = request.json.get("email")
        oldpassword = request.json.get("oldpassword")
        newpassword = request.json.get("newPassword")

        # Check Parameter Exictence
        if (email == None or oldpassword == None or newpassword == None):
            return {"message":"Missing Parameter"},406

        # Check Password
        query = f"SELECT password FROM User WHERE email = '{email}'"
        cursor.execute(query)
        user_password = cursor.fetchone()[0]
        print(f"New {newpassword} Old: {oldpassword}, real: {user_password}")
        if(user_password != oldpassword):
            return {"message":"Wrong Password"},406
        
        # Insert a new user into the Users table
        query = f"UPDATE User SET password = '{newpassword}' WHERE email = '{email}'"
        cursor.execute(query)
        myDB.commit()
        
        cursor.close()
        return jsonify({"message":"Password Changed"}), 200
    except:
        cursor.close()
        return jsonify({'message': "Somthing went Wrong"}), 406

