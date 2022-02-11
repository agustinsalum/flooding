from flask import render_template, url_for, request, redirect, session
from app.models.usuario import Usuario
from app.models.configuracion import Configuracion
from app.helpers import auth

def login():
    if request.method == 'POST':    
        session.clear()
        params  = request.form
        usuario = Usuario.query.filter_by(email=params['email']).first()
        if usuario:
            configuracion = Configuracion.obtener_configuracion()
            t = usuario.verificar_clave(params['clave'])
            if usuario.verificar_clave(params['clave']):
                mensaje = "Se logueo correctamente"
                session['usuario'] = usuario
                return redirect(url_for('index'))  
            else:
                mensaje = "Las credenciales no son válidas. Vuelva a intentarlo"
                return render_template('/auth/login.html', mensaje=mensaje, configuracion=configuracion)        
        else:
            mensaje = "Las credenciales no son válidas. Vuelva a intentarlo"
            return render_template('/auth/login.html', mensaje=mensaje)
    else:
        if auth.authenticated(session):
            return redirect(url_for('index'))
        else:
            return render_template('/auth/login.html')




def logout():
    session.clear()
    return redirect(url_for('index'))