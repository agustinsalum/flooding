from flask import render_template, url_for, request, redirect, session
from app.helpers import permisos
from app.models.recorrido import Recorrido
from app.models.configuracion import Configuracion
from app.validaciones.validar_recorrido import ValidarRecorrido

def listado(nombre=' ', estado='todos', page=1):
    permisos.validar_permisos('recorrido_index')
    per_page = Configuracion.obtener_configuracion().cantidad_elementos_pagina
    recorridos_actuales = Recorrido.todo()
    if (not recorridos_actuales):
        mensaje_sin_recorridos = "No existen recorridos cargados en este momento"
        return render_template("recorrido/listado.html", recorridos_actuales=recorridos_actuales, mensaje_sin_recorridos=mensaje_sin_recorridos)
    recorridos_actuales = recorridos_actuales[0]
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
        recorridos_actuales = recorridos_actuales.query.order_by(Recorrido.nombre.desc())
    else:
        recorridos_actuales = recorridos_actuales.query.order_by(Recorrido.nombre.asc())

    if nombre_alternativo != ' ':
        recorridos_actuales = recorridos_actuales.filter(Recorrido.nombre.like('%' + nombre_alternativo + '%'))
    if estado_alternativo != 'todos':
        recorridos_actuales = recorridos_actuales.filter_by(estado = estado_alternativo)
    recorridos_actuales = recorridos_actuales.paginate(per_page=per_page)
    return render_template("recorrido/listado.html", recorridos_actuales = recorridos_actuales, nombre = nombre_alternativo, estado = estado_alternativo)


def agregar_recorrido():
    permisos.validar_permisos('recorrido_create')    
    if request.method == 'POST':
        #Para obtener un campo especifico es request.form.get('nombre')
        datos_recorrido = request.form
        mensaje = ''
        errores = ValidarRecorrido(datos_recorrido).validar()
        if not errores:
            Recorrido.crear(datos_recorrido['nombre'],
                datos_recorrido['descripcion'],
                datos_recorrido['estado'],
                datos_recorrido['arreglo_coordenadas'])           
            mensaje = "Recorrido creado exitosamente"
            return render_template('recorrido/crear_recorrido.html', mensaje=mensaje)
        else:
            return render_template('recorrido/crear_recorrido.html', errores=errores)
    else:
        # En la primera entra aca
        return render_template('recorrido/crear_recorrido.html', )

def borrar_recorrido(id):
    permisos.validar_permisos('recorrido_destroy')
    Recorrido.borrar_recorrido(id)
    return redirect(url_for('listado_recorrido'))

def publicar_recorrido(id):
    permisos.validar_permisos('recorrido_update')
    Recorrido.publicar_recorrido(id)
    return redirect(url_for('listado_recorrido'))

def despublicar_recorrido(id):
    permisos.validar_permisos('recorrido_destroy')
    Recorrido.despublicar_recorrido(id)
    return redirect(url_for('listado_recorrido'))

def editar_recorrido(id):
    permisos.validar_permisos('recorrido_update')
    recorrido = Recorrido.obtener_por_id(id)
    mensaje = ''
    if request.method == 'POST':
        datos_nuevos_recorrido = request.form        
        Recorrido.editar(id, datos_nuevos_recorrido['nombre'], datos_nuevos_recorrido['coords'], datos_nuevos_recorrido['descripcion'])            
        mensaje = "Recorrido editado exitosamente"
        return render_template('recorrido/editar_recorrido.html', recorrido=recorrido, mensaje=mensaje)        
    else:
        return render_template('recorrido/editar_recorrido.html', recorrido=recorrido, mensaje=mensaje)       