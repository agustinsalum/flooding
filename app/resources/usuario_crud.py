from flask import render_template, url_for, request, redirect
from app.models.usuario import Usuario
from app.validaciones.validar_usuario import ValidarUsuario 
from app.helpers import permisos
from app.models.configuracion import Configuracion
from app.models.rol import Rol



def tiene_permiso(usuario, nombre_permiso):
    resultado = False
    for rol in usuario.roles:
        for permiso in rol.permisos:
            if permiso.nombre == nombre_permiso:
                resultado = True
        return resultado


def agregar_usuario():
    permisos.validar_permisos('usuario_new')
    roles= Rol.todo()
    if request.method == 'POST':
        #Para obtener un campo especifico es request.form.get('nombre')
        datos_usuario = request.form
        mensaje = ''
        errores = ValidarUsuario(datos_usuario).validar()
        if not errores:
            Usuario.crear(datos_usuario['usuario'],
                datos_usuario['clave'],
                datos_usuario['nombre'],
                datos_usuario['apellido'],
                datos_usuario['email'],
                datos_usuario['roles'])
            mensaje = "Usuario creado exitosamente"
            return render_template('user/crear_usuario.html', mensaje=mensaje, roles=roles)
        else:
            return render_template('user/crear_usuario.html', mensaje=mensaje, roles=roles, errores=errores)
    else:
        # En la primera entra aca
        return render_template('user/crear_usuario.html', roles=roles)


# Edicion de un usuario seleccionado en la lista
def editar_usuario(id):
    permisos.validar_permisos('usuario_update')
    usuario = Usuario.obtener_por_id(id)
    roles = Rol.todo()
    mensaje = ''
    if request.method == 'POST':
        datos_nuevos_usuario = request.form        
        #chequea que no exista ya el nombre de usuario y el email
        if ValidarUsuario(datos_nuevos_usuario).existe_usuario() and not datos_nuevos_usuario['usuario'] == usuario.usuario:
            mensaje="El Nombre de Usuario ya existe"
        elif ValidarUsuario(datos_nuevos_usuario).existe_email() and not datos_nuevos_usuario['email'] == usuario.email:
            mensaje="El E-Mail ya existe"
        else:
            nuevos_roles = request.form.getlist("roles")            
            Usuario.editar(id, datos_nuevos_usuario['usuario'],
                datos_nuevos_usuario['nombre'],
                datos_nuevos_usuario['apellido'],
                datos_nuevos_usuario['email'],
                nuevos_roles)            
            mensaje = "Usuario editado exitosamente"                            
        return render_template('user/editar_usuario.html', usuario=usuario, mensaje=mensaje, roles=roles)        
    else:
        return render_template('user/editar_usuario.html', usuario=usuario, mensaje=mensaje,roles=roles)
       

def ver_perfil():
    return render_template('user/ver_perfil.html')


def cambiar_password(id):
    permisos.validar_permisos('usuario_update')
    usuario = Usuario.obtener_por_id(id)    
    mensaje = ''
    if request.method == 'POST':
        datos_nuevos = request.form        
        Usuario.editar_contraseña(id, datos_nuevos['passwordnuevo'])            
        mensaje = "Password cambiada exitosamente"
        usuarios = Usuario.todo()                         
        return redirect(url_for('cambiar_password', id=id))                
    else:
        return render_template('user/cambiar_password.html', usuario=usuario, mensaje=mensaje)
    

def activar(id):
    permisos.validar_permisos('usuario_update')
    Usuario.activar_usuario(id)
    return redirect(url_for('listado_usuarios'))

def desactivar(id):
    permisos.validar_permisos('usuario_destroy')
    Usuario.desactivar_usuario(id)
    return redirect(url_for('listado_usuarios'))

def listado(nombre=' ', estado='todos' , page=1):
    permisos.validar_permisos('usuario_index')
    per_page = Configuracion.obtener_configuracion().cantidad_elementos_pagina
    usuarios_actuales_activos = Usuario.todo()
    if (not usuarios_actuales_activos):
        mensaje_sin_usuarios = "No existen usuarios cargados en este momento"
        return render_template("user/listado.html", usuarios_actuales_activos=usuarios_actuales_activos, mensaje_sin_usuarios=mensaje_sin_usuarios)
    usuarios_actuales_activos = usuarios_actuales_activos[0]
    if request.method == 'GET':
        if request.args:
            params = request.args
            if params['estado']:
                estado_alternativo= params['estado']
            else:
                estado_alternativo = estado
            if params['nombre']:
                nombre_alternativo= params['nombre']
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
        usuarios_actuales_activos = usuarios_actuales_activos.query.order_by(Usuario.nombre.desc())
    else:
        usuarios_actuales_activos = usuarios_actuales_activos.query.order_by(Usuario.nombre.asc())

    if nombre_alternativo != ' ':
        usuarios_actuales_activos = usuarios_actuales_activos.filter(Usuario.nombre.like('%' + nombre_alternativo + '%'))
    if estado_alternativo != 'todos':
        usuarios_actuales_activos = usuarios_actuales_activos.filter_by(activo = estado_alternativo)
    usuarios_actuales_activos = usuarios_actuales_activos.paginate(page, per_page=per_page)
    return render_template("user/listado.html", usuarios_actuales_activos=usuarios_actuales_activos, nombre = nombre_alternativo, estado = estado_alternativo)
