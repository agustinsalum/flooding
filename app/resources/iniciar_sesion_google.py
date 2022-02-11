# IMPORTACIONES
import os

from flask import render_template, session, url_for
from app import db
from app.models.configuracion import Configuracion
from flask import request, redirect
import requests
from oauthlib.oauth2 import WebApplicationClient
import json
from os import environ
from app.models.usuario_google import UsuarioGoogle
from config import config

# CLAVES PRIVADAS DE GOOGLE
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# claves privadas eliminadas
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Nuestra aplicacion cliente que llama a google debe tener el id del cliente

client = WebApplicationClient(GOOGLE_CLIENT_ID)
env = environ.get("FLASK_ENV", "development")


# FUNCIONES

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def login_with_google_iniciar():
    print ("ENTRASTE A LOGIN INICIAR")
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=config[env].GOOGLE_REDIRECT_URI_INICIO,
        # Elementos predefinidos para que los proveedores nos brinden
        # email nos devuelve el mail
        # profile nos devuelve nombre,apellido, foto de perfil..etc
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


def callback_iniciar():
    # Get authorization code Google sent back to you
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

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # Si google nos autoriza podemos acceder a todos estos valores
    if userinfo_response.json().get("email_verified"):
        #id = userinfo_response.json()["sub"]
        correo = userinfo_response.json()["email"]
        nombre = userinfo_response.json()["given_name"]
        apellido = userinfo_response.json()["family_name"]
 
    else:
        return "User email not available or not verified by Google.", 400

    
    user_google = UsuarioGoogle.existe_correo(correo)
    mensaje_error = ""
    # El correo ya esta activo o pendiente
    if UsuarioGoogle.esta_aprobado(user_google.id):
        configuracion = Configuracion.obtener_configuracion()
        session.clear()
        session['usuario'] = user_google
        return redirect(url_for('index'))  
    else:
        mensaje_error= "Usted por el momento no fue aceptado. Debe esperar la confirmacion de un administrador"
        return render_template('auth/login.html', mensaje_error=mensaje_error)
          