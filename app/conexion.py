import mysql.connector
from os import environ

# Conectamos con mysql. Datos sensibles en el .env
def conexion():
    from config import config
    env = environ.get("FLASK_ENV", "development")
    mydb = mysql.connector.connect(
        host = config[env].DB_HOST,
        user = config[env].DB_USER,
        password = config[env].DB_PASS
    )
    mycursor = mydb.cursor()
    # Creamos la base de datos con el nombre grupo39
    mycursor.execute("CREATE DATABASE flooding")