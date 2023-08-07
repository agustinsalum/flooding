from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from app.conexion import conexion

db = SQLAlchemy()

def init_app(app):
    config_db(app)


def config_db(app):
    from app.cargar_datos import cargar

    with app.app_context():
        # Creamos la base de datos. Se crean todos los modelos
        try:
            conexion()
            #db.drop_all() # Elimina todas las tablas
            db.create_all() # Crea todas las tablas
            cargar(db) # Carga los datos de las tablas
        # La base de datos ya existe o "err" nos detallara otro posible error
        except mysql.connector.Error as err:
            print(f"Entro al except por: {err}")