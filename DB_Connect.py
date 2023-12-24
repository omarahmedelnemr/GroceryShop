import mysql.connector
from decouple import config


# MySQL configuration
myDB = mysql.connector.connect(
    host     = config("DB_HOST"),
    port     = config("DB_PORT"),
    user     = config("DB_USER"),
    password = config("DB_PASS"),
    database = config("DB_NAME")    
)