
# Importaciones flask

from flask import Flask, render_template
from flask_session import Session
from os import name, path, environ
from flask_cors import CORS
from config import config
from app import db

# Importaciones resources

from app.resources import configuracion, iniciar_sesion_google, registrarse_google, usuario_autenticacion, usuario_crud, usuario_google, punto_encuentro, recorrido, zonas, denuncia
from app.resources.api import denuncias, puntodeencuentro, recorridoevacuacion
from app.resources.api import zonasinundables

# Otras importaciones

from app.db import db, init_app
from app.models.configuracion import Configuracion
from app.helpers import permisos
from app.helpers import auth
from app.helpers import configuracion_colores


# Importaciones OAuth

from oauthlib.oauth2 import WebApplicationClient
from flask_login import LoginManager

# CLAVES PRIVADAS DE GOOGLE
GOOGLE_CLIENT_ID = '853530354298-3hcp4cuv55hkjsphdsquknunb0tid1q1.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    
    # Política de seguridad en los navegadores
    CORS(app)


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


    #init_app(app)

    #OAuth
    app.secret_key = 'randomsecretkey'
    
    # OAuth 2 client setup
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.get(user_id)
    
    #FIN OAuth

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    Session(app)
    # Configuracion de la BD
    app.secret_key = 'hola'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + \
        app.config["DB_USER"]+":"+app.config["DB_PASS"]+"@"+app.config["DB_HOST"]+"/"+app.config["DB_NAME"]
    db.init_app(app)
    



    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    app.jinja_env.globals.update(permisos=permisos)
    app.jinja_env.globals.update(auth=auth)
    app.jinja_env.globals.update(configuracion_colores=configuracion_colores)
    

    # Autenticacion
    app.add_url_rule('/login', 'login', usuario_autenticacion.login, methods=["GET", "POST"])
    app.add_url_rule('/logout', 'logout', usuario_autenticacion.logout)

    # Endpoints para Configuracion del Sitio
    app.add_url_rule('/configuracion/vista_configuracion', 'vista_configuracion',
                     configuracion.vista_configuracion, methods=["POST", "GET"])

    # Endpoints para Listado de usuarios

    app.add_url_rule('/user/listado', 'listado_usuarios', usuario_crud.listado, methods=["GET", "POST"])

    app.add_url_rule('/user/listado/<int:page>', 'listado',
                     usuario_crud.listado, methods=["POST", "GET"])
    
    # Endpoints para Listado de usuarios de google

    app.add_url_rule('/google/listado', 'listado_usuarios_google', usuario_google.listado, methods=["GET", "POST"])

    # Endpoints para aprobar usuarios de google
    app.add_url_rule('/user/aprobar_usuario/<id>', 'aprobar_usuario',
                    usuario_google.aprobar_usuario, methods=['POST', 'GET'])


    # Endpoints para agregar un nuevo usuario
    app.add_url_rule('/user/agregar_usuario', 'agregar_usuario',
                     usuario_crud.agregar_usuario, methods=["POST", "GET"])
                     

    # Endpoints para Editar usuario
    app.add_url_rule('/user/editar_usuario/<id>', 'editar_usuario',
                    usuario_crud.editar_usuario, methods=['POST', 'GET'])

    # Endpoints para Editar perfil
    app.add_url_rule('/user/ver_perfil', 'ver_perfil',
                    usuario_crud.ver_perfil, methods=['POST', 'GET']) 
      
    # Endpoints para Activar un usuario
    app.add_url_rule('/user/activar/<id>', 'activar',
                     usuario_crud.activar,  methods=['POST', 'GET'])
    # Endpoints para Desactivar un usuario
    app.add_url_rule('/user/desactivar/<id>', 'desactivar',
                    usuario_crud.desactivar,  methods=['POST', 'GET'])
    
    # Endpoints para cambiar password
    app.add_url_rule('/user/cambiar_password/<id>', 'cambiar_password',
                    usuario_crud.cambiar_password, methods=['POST', 'GET']) 
    
    # PUNTOS DE ENCUENTRO 
    app.add_url_rule('/puntos/listado', 'administrar_puntos',
                     punto_encuentro.listado, methods=["GET", "POST"])
    
    app.add_url_rule('/puntos/listado/<int:page>', 'administrar_puntos',
                     punto_encuentro.listado, methods=["POST", "GET"])


                       
    # Endpoints para agregar un nuevo punto de encuentro
    app.add_url_rule('/puntos/agregar_punto', 'agregar_punto',
                     punto_encuentro.agregar_punto, methods=["POST", "GET"])
    
     # Endpoints para Editar un punto de encuentro
    app.add_url_rule('/punto/editar_punto/<id>', 'editar_punto',
                     punto_encuentro.editar_punto, methods=['POST', 'GET'])
    # Endpoints para publicar punto
    app.add_url_rule('/punto/publicar/<id>', 'publicar',
                     punto_encuentro.publicar,  methods=['POST', 'GET'])
    # Endpoints para Despublicar punto
    app.add_url_rule('/punto/despublicar/<id>', 'despublicar',
                     punto_encuentro.despublicar,  methods=['POST', 'GET'])
    
    # Endpoints para Eliminar un punto de encuentro
    app.add_url_rule('/punto/borrar_punto/<id>', 'borrar_punto',
                     punto_encuentro.borrar_punto, methods=['POST', 'GET'])
    
    # Endpoints para agregar una nueva denuncia
    app.add_url_rule('/denuncia/crear_denuncia', 'agregarDenuncia',
                     denuncia.crear_denuncia, methods=["POST", "GET"])  
    
    # Endpoints para validar una denuncia
    app.add_url_rule('/denuncia/validar_denuncia/<id>', 'validar_denuncia',
                     denuncia.validar_denuncia, methods=["POST", "GET"])

    # Endpoints para asignarme una denuncia
    app.add_url_rule('/denuncia/asignarme_denuncia/<id>', 'asignarme_denuncia',
                     denuncia.asignarme_denuncia, methods=["POST", "GET"])

    # Endpoints para asignar una denuncia a un usuario
    app.add_url_rule('/denuncia/asignar_denuncia_usuario/<id>', 'asignar_denuncia_usuario',
                     denuncia.asignar_denuncia_usuario, methods=["POST", "GET"])
       
    # Endpoints para validar las denuncias 
    app.add_url_rule('/denuncia/listado_seguimiento', 'listado_seguimiento',
                     denuncia.listado_seguimiento, methods=["POST", "GET"])
    
    app.add_url_rule('/denuncia/listado_seguimiento/<int:page>', 'listado_seguimiento',
                     denuncia.listado_seguimiento, methods=["POST", "GET"])
    
    # Endpoints listado de denuncias 
    app.add_url_rule('/denuncia/listado', 'denuncias',
                     denuncia.listado, methods=["GET", "POST"])
    
    app.add_url_rule('/denuncia/listado/<int:page>', 'denuncias',
                     denuncia.listado, methods=["POST", "GET"])
    
    # Endpoints para Editar denuncia
    app.add_url_rule('/denuncia/editar_denuncia/<id>', 'editar_denuncia',
                    denuncia.editar_denuncia, methods=['POST', 'GET'])

    # Endpoints para Eliminar una denuncia
    app.add_url_rule('/punto/borrar_denuncia/<id>', 'borrar_denuncia',
                     denuncia.borrar_denuncia, methods=['POST', 'GET'])
    
    # RECORRIDOS DE EVACUACION 
    app.add_url_rule('/recorrido/listado', 'listado_recorrido',
                     recorrido.listado, methods=["GET", "POST"])
    
    app.add_url_rule('/recorrido/listado/<int:page>', 'listado_recorrido',
                     recorrido.listado, methods=["POST", "GET"])

    # Endpoints para agregar una nueva recorrido de evacuación
    app.add_url_rule('/recorrido/agregar_recorrido', 'agregar_recorrido',
                     recorrido.agregar_recorrido, methods=["POST", "GET"])
    
    # Endpoints para Eliminar un recorrido de evacuación
    app.add_url_rule('/recorrido/borrar_recorrido/<id>', 'borrar_recorrido',
                     recorrido.borrar_recorrido, methods=['POST', 'GET'])
    
    # Endpoints para publicar recorrido
    app.add_url_rule('/recorrido/publicar/<id>', 'publicar_recorrido',
                     recorrido.publicar_recorrido,  methods=['POST', 'GET'])

    # Endpoints para Despublicar recorrido
    app.add_url_rule('/recorrido/despublicar/<id>', 'despublicar_recorrido',
                     recorrido.despublicar_recorrido,  methods=['POST', 'GET'])
    
    # Endpoints para Editar recorrido
    app.add_url_rule('/recorrido/editar_recorrido/<id>', 'editar_recorrido',
                    recorrido.editar_recorrido, methods=['POST', 'GET'])
    
    # AUTHLIB

    app.add_url_rule('/auth/login', 'registrarse_google',
                     registrarse_google.login_with_google_registro, methods=["GET", "POST"])
    app.add_url_rule('/auth/login/callback', "auth_callback_registro", registrarse_google.callback, methods=["GET"]
    )

    app.add_url_rule('/auth/login/iniciar_sesion', 'iniciar_sesion_google',
                     iniciar_sesion_google.login_with_google_iniciar, methods=["GET", "POST"])
    app.add_url_rule('/auth/login/iniciar_sesion/callback_iniciar', "auth_callback_iniciar", iniciar_sesion_google.callback_iniciar, methods=["GET"]
    )
    

    

     # Endpoints para la api
    app.add_url_rule('/api/denuncia/<int:id>', 'mostrar_denuncia',denuncias.mostrar_denuncia, methods=['GET'])
    app.add_url_rule('/api/denuncias/page', 'mostrar_denuncias',denuncias.mostrar_denuncias, methods=['GET'])
    app.add_url_rule('/api/zonas-inundables/<int:id>/', 'mostrar_zona',zonasinundables.mostrar_zona, methods=['GET'])
    app.add_url_rule('/api/zonas-inundables', 'mostrar_zonas',zonasinundables.mostrar_zonas, methods=['GET'])
    app.add_url_rule('/api/crear_denuncia','crear_denuncia',denuncias.crear_denuncia, methods=['POST'])
    app.add_url_rule('/api/punto/<int:id>', 'mostrar_punto',puntodeencuentro.mostrar_punto, methods=['GET'])
    app.add_url_rule('/api/puntos-encuentro', 'mostrar_puntos',puntodeencuentro.mostrar_puntos, methods=['GET'])
    app.add_url_rule('/api/recorrido/<int:id>', 'mostrar_recorrido',recorridoevacuacion.mostrar_recorrido, methods=['GET'])
    app.add_url_rule('/api/recorridos-evacuacion', 'mostrar_recorridos',recorridoevacuacion.mostrar_recorridos , methods=['GET'])
    


    # Zonas inundables
    app.add_url_rule('/zonas', 'zonas_index',
                     zonas.index, methods=['POST', 'GET'])

    app.add_url_rule('/zonas/import', 'zonas_upload',
                     zonas.upload, methods=['POST', 'GET'])

    # Endpoints para Editar usuario
    app.add_url_rule('/zonas/editar_zona/<id>', 'editar_zona',
                    zonas.editar_zona, methods=['POST', 'GET'])

    # Endpoints para Editar zona
    app.add_url_rule('/zonas/ver_zona', 'ver_zona',
                    zonas.ver_zona, methods=['POST', 'GET']) 
      
    # Endpoints para Activar un zona
    app.add_url_rule('/zonas/activar/<id>', 'activar_zona',
                     zonas.activar,  methods=['POST', 'GET'])
    # Endpoints para Desactivar un zona
    app.add_url_rule('/zonas/desactivar/<id>', 'desactivar_zona',
                    zonas.desactivar,  methods=['POST', 'GET'])
  # Endpoints para Desactivar un zona
    app.add_url_rule('/zonas/eliminar/<id>', 'delete_zona',
                    zonas.eliminar,  methods=['POST', 'GET'])



 # Manejo de errores
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errores/404.html'), 404

    @app.errorhandler(503)
    def page_not_found(e):
        return render_template('errores/503.html'), 503

    @app.errorhandler(401)
    def page_not_found(e):
        return render_template('errores/401.html'), 401

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('errores/403.html'), 403



    @app.route('/')
    def index():
        init_app(app)
        configuracion = Configuracion.obtener_configuracion()
        return render_template('index.html', configuracion=configuracion)
    return app