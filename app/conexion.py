import mysql.connector
from os import environ

# Conectamos con mysql. Datos sensibles en el .env
def conexion():
    from config import config
    env = environ.get("FLASK_ENV", "development")
    # Otra opcion podria ser importando import mysql.connector as mariadb y usando mariadb.connect
    mydb = mysql.connector.connect(
        host= config[env].SQLALCHEMY_HOST,
        user= config[env].SQLALCHEMY_USER,
        password= config[env].SQLALCHEMY_PASS
    )
    mycursor = mydb.cursor()
    # Creamos la base de datos con el nombre grupo39
    mycursor.execute("CREATE DATABASE grupo39")