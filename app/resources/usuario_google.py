
from app.helpers import permisos
from flask import render_template, request
from app.models.rol import Rol
from app.models.usuario_google import UsuarioGoogle
from app.models.configuracion import Configuracion


def listado(nombre=' ', estado='todos', page=1):
    permisos.validar_permisos('usuario_index')
    per_page = Configuracion.obtener_configuracion().cantidad_elementos_pagina
    usuarios_google = UsuarioGoogle.todo()
    if (not usuarios_google):
        mensaje_sin_usuarios = "No existen usuarios cargados en este momento"
        return render_template("google/listado.html", usuarios_google=usuarios_google, mensaje_sin_usuarios=mensaje_sin_usuarios)
    usuarios_google = usuarios_google[0] 
    print (usuarios_google)
    if request.method == 'GET':
        if request.args:
            params = request.args
            if params['estado']:
                estado_alternativo= params['estado']
            else:
                estado_alternativo = estado
            if params['nombre']:
                nombre_alternativo = params['nombre']
            else:
                nombre_alternativo = nombre
        else:
            estado_alternativo = estado
            nombre_alternativo = nombre
    if request.method == 'POST':
        page=1
        params = request.form
        nombre_alternativo = params['nombre']
        estado_alternativo = params['estado']
    orden = Configuracion.obtener_configuracion().criterio_ordenacion
    if orden == 'desc': 
        usuarios_google = usuarios_google.query.order_by(UsuarioGoogle.nombre.desc())
    else:
        usuarios_google = usuarios_google.query.order_by(UsuarioGoogle.nombre.asc())

    if nombre_alternativo != ' ':
        usuarios_google = usuarios_google.filter(UsuarioGoogle.nombre.like('%' + nombre_alternativo + '%'))
    if estado_alternativo != 'todos':
        usuarios_google = usuarios_google.filter_by(aprobado = estado_alternativo)
    usuarios_google = usuarios_google.paginate(per_page=per_page)
    return render_template("google/listado.html", usuarios_google=usuarios_google, nombre = nombre_alternativo, estado = estado_alternativo)


#Edicion de un usuario seleccionado en la lista
def aprobar_usuario(id):
    permisos.validar_permisos('usuario_google')
    usuario = UsuarioGoogle.obtener_por_id(id)
    roles   = Rol.todo()
    mensaje = ''
    if request.method == 'POST':
        roles_asignados = request.form.getlist("roles")
        if (len(roles_asignados) == 0):
            mensaje = "Debe seleccionar al menos un rol"
            return render_template('google/aprobar_usuario.html', usuario=usuario, mensaje=mensaje, roles=roles)
        else:
            UsuarioGoogle.aprobar(id, roles_asignados)
            mensaje = "El usuario fue aceptado"
            return render_template('google/aprobar_usuario.html', usuario=usuario, mensaje=mensaje, roles=roles)        
    else:
        return render_template('google/aprobar_usuario.html', usuario=usuario,roles=roles)