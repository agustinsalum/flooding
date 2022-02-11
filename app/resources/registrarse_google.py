# IMPORTACIONES
from os import environ
from flask import render_template
from app.validaciones.validar_usuario_google import ValidarUsuarioGoogle 
from flask import request, redirect
import requests
from oauthlib.oauth2 import WebApplicationClient
import json
from app.models.usuario import Usuario
from app.models.usuario_google import UsuarioGoogle
from config import config

# CLAVES PRIVADAS DE GOOGLE
# Oauth2 funciona a traves de la capa SSL
# si su servidor no esta parametrizado para permitir HTTPS, el metodo fetch_token generara un error
# error InsecureTransportError lo cual lo desactivamos
environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = '853530354298-3hcp4cuv55hkjsphdsquknunb0tid1q1.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Nuestra aplicacion cliente que llama a google debe tener el id del cliente
# cliente que maneja el codigo de autorizacion
client = WebApplicationClient(GOOGLE_CLIENT_ID)
env = environ.get("FLASK_ENV", "development")
# FUNCIONES

def generar_nombre_usuario(correo):
    lista = correo.split("@")
    return lista[0]

# retorna
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def login_with_google_registro():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    

    #Utilice la biblioteca para construir la solicitud de inicio de sesion de Google y proporcionar ambitos que le permiten recuperar el perfil del usuario de google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        # Definimos las rutas aca porque para cada uno vamos a tener valores distintos
        # Google se debe conectar con ambos casos
        redirect_uri=config[env].GOOGLE_REDIRECT_URI_REGISTRO,
        # Elementos predefinidos para que los proveedores nos brinden
        # email nos devuelve el mail
        # profile nos devuelve nombre,apellido, foto de perfil..etc
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

# Ya tenemos la llamada y google chequea que nuestra aplicacion sea valida, con el client id y secret
def callback():
    # Reciba el codigo de autorizacion que le envio google
    # Nos devuelve un codigo con el cual podemos construir el pedido de autorizacion al usuario
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # !analiza los tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # Si google nos autoriza podemos acceder a todos estos valores
    # Dependiendo del scote podemos obtener mas atributos
    if userinfo_response.json().get("email_verified"):
        #id = userinfo_response.json()["sub"]
        correo = userinfo_response.json()["email"]
        nombre = userinfo_response.json()["given_name"]
        apellido = userinfo_response.json()["family_name"]
 
    else:
        return "User email not available or not verified by Google.", 400
    
    nombre_usuario = generar_nombre_usuario(correo)
    user_google = UsuarioGoogle.existe_correo(correo)
    user = Usuario.obtener_por_correo(correo)
    mensaje_pendiente = ""
    mensaje_error = ""
    # Si el correo no esta registrado entonces validamos y lo ponemos pendiente
    errores = ValidarUsuarioGoogle(nombre_usuario,correo).validar()
    if  (user is None) & (user_google is None):
        if not errores:
            UsuarioGoogle.crear_pendiete(nombre_usuario, nombre, apellido, correo)
            mensaje_pendiente = "Su solicitud de registro fue enviada!! debe esperar la confirmacion de un administrador"
            # Volvemos al login
            return render_template('auth/login.html', mensaje_pendiente=mensaje_pendiente)
        else:
            # Ocurrio un problema en la validacion
            return render_template('auth/login.html', mensaje_pendiente=mensaje_pendiente, errores=errores)
    # El correo ya esta activo o pendiente
    else:
        if UsuarioGoogle.esta_aprobado(user_google.id):
            mensaje_error= "Usted ya solicito un registro y fue aprobada. Por favor, inicie sesion"
            return render_template('auth/login.html', mensaje_error=mensaje_error) 
        else:
            mensaje_error= "Usted ya envio la solicitud de registro. Debe esperar la confirmacion de un administrador"
            return render_template('auth/login.html', mensaje_error=mensaje_error)
          