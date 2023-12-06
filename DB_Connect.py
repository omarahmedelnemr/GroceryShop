import mysql.connector


# MySQL configuration
myDB = mysql.connector.connect(
    host = 'mysql-156876-0.cloudclusters.net',
    port = 10026,
    user = 'admin',
    password = '7TE9ESeh',
    database = 'GroceryShop'    
)