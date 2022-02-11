from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from app.conexion import conexion

db = SQLAlchemy()

def init_app(app):
    config_db(app)


def config_db(app):
    from app.cargar_datos import cargar

    @app.before_first_request
    def init_database():
        # Creamos la base de datos. Se crean todos los modelos
        try:
            conexion()
            #db.drop_all() # Elimina todas las tablas
            db.create_all() # Crea todas las tablas
            cargar(db) # Carga los datos de las tablas
        # Si va por el except, significa que la base de datos ya existe
        except mysql.connector.Error:
            pass # declaración nula
    @app.teardown_request
    def close_session(exeption=None):
        db.session.remove()