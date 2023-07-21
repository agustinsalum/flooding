from os import environ

class Config(object):
    """Base configuration."""

    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"
    SECRET_KEY = "secret"

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass

# Se ejecuta en Producccion
class ProductionConfig(Config):
    """Production configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "nombre_user_producccion")
    DB_PASS = environ.get("DB_PASS", "contraseña_producccion")
    DB_NAME = environ.get("DB_NAME", "nombre_db_producccion")

    # GOOGLE DEL LADO DE PRODUCCION
    # CALLBACK es una funcion extensible que se ejecuta luego del suceso de un evento
    GOOGLE_REDIRECT_URI_REGISTRO = environ.get("GOOGLE_REDIRECT_URI_REGISTRO", "https://admin-grupo39.proyecto2021.linti.unlp.edu.ar/auth/login/callback")
    GOOGLE_REDIRECT_URI_INICIO   = environ.get("GOOGLE_REDIRECT_URI_INICIO", "https://admin-grupo39.proyecto2021.linti.unlp.edu.ar/auth/login/iniciar_sesion/callback_iniciar")

    # CREAR BASE DE DATOS CON SQLALCHEMY DEL LADO DE PRODUCCION
    SQLALCHEMY_HOST = environ.get("SQLALCHEMY_HOST", "localhost")
    SQLALCHEMY_USER = environ.get("SQLALCHEMY_USER", "nombre_user_producccion")
    SQLALCHEMY_PASS = environ.get("SQLALCHEMY_PASS", "contraseña_producccion")


# Se ejecuta en Desarrollo
class DevelopmentConfig(Config):
    """Development configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")

    
    # GOOGLE DEL LADO LOCAL
    GOOGLE_REDIRECT_URI_REGISTRO = environ.get("GOOGLE_REDIRECT_URI_REGISTRO", None)
    GOOGLE_REDIRECT_URI_INICIO   = environ.get("GOOGLE_REDIRECT_URI_INICIO", None)

    # CREAR BASE DE DATOS CON SQLALCHEMY DEL LADO LOCAL
    SQLALCHEMY_HOST = environ.get("SQLALCHEMY_HOST", None)
    SQLALCHEMY_USER = environ.get("SQLALCHEMY_USER", None)
    SQLALCHEMY_PASS = environ.get("SQLALCHEMY_PASS", None)



class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")


config = dict(
    development=DevelopmentConfig, test=TestingConfig, production=ProductionConfig
)

## More information
# https://flask.palletsprojects.com/en/2.3.x/config/#configuring-from-environment-variables