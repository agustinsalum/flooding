
from flask import render_template, url_for, request, redirect
from app.models.configuracion import Configuracion
from app.helpers import permisos
from app.models.punto_encuentro import PuntoEncuentro
from app.validaciones.validar_punto import ValidarPunto   
  

def listado(nombre=' ', estado='todos', page=1):
    permisos.validar_permisos('punto_encuentro_index')
    per_page = Configuracion.obtener_configuracion().cantidad_elementos_pagina
    puntosActuales = PuntoEncuentro.todo()
    if (not puntosActuales):
        mensaje_sin_puntos = "No existen puntos de encuentro cargados en este momento"
        return render_template("puntos/listado.html", puntosActuales=puntosActuales, mensaje_sin_puntos=mensaje_sin_puntos)
    puntosActuales = puntosActuales[0]
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
        puntosActuales = puntosActuales.query.order_by(PuntoEncuentro.nombre.desc())
    else:
        puntosActuales = puntosActuales.query.order_by(PuntoEncuentro.nombre.asc())

    if nombre_alternativo != ' ':
        puntosActuales = puntosActuales.filter(PuntoEncuentro.nombre.like('%' + nombre_alternativo + '%'))
    if estado_alternativo != 'todos':
        puntosActuales = puntosActuales.filter_by(estado = estado_alternativo)
    puntosActuales = puntosActuales.paginate(page, per_page=per_page)

    return render_template("puntos/listado.html", puntosActuales=puntosActuales, nombre = nombre_alternativo, estado = estado_alternativo)


def agregar_punto():
    permisos.validar_permisos('punto_encuentro_new')
    if request.method == 'POST':
        datos_punto = request.form
        mensaje = ''
        errores = ValidarPunto(datos_punto).validar()
        if not errores:
            PuntoEncuentro.crear(datos_punto['nombre'],
                datos_punto['direccion'],
                datos_punto['latitud'],
                datos_punto['longitud'],
                datos_punto['estado'],
                datos_punto['telefono'],
                datos_punto['email'])
            mensaje = "punto de encuentro creado exitosamente"
            return render_template('puntos/crear_punto.html', mensaje=mensaje)
        else:
            return render_template('puntos/crear_punto.html', errores=errores)
    else:
        return render_template('puntos/crear_punto.html')


#Edicion de un punto
def editar_punto(id):
    permisos.validar_permisos('punto_encuentro_update')
    punto = PuntoEncuentro.obtener_por_id(id)
    mensaje = ''
    if request.method == 'POST':
        datos_nuevos_punto = request.form
        errores = ValidarPunto(datos_nuevos_punto).validar()
        # Si no modifico su titulo y el correo eliminamos esos error
        if punto.nombre == datos_nuevos_punto['nombre']:
            del errores["Error por nombre repetido"]
        if punto.email == datos_nuevos_punto['email']:
            del errores["Error con el correo"]
        if not errores:
            PuntoEncuentro.editar(id, datos_nuevos_punto['nombre'],
                datos_nuevos_punto['direccion'],
                datos_nuevos_punto['telefono'],
                datos_nuevos_punto['email'],
                datos_nuevos_punto['latitud'],
                datos_nuevos_punto['longitud'] )
            mensaje = "Punto editado exitosamente"
            return render_template('puntos/editar_punto.html', punto=punto, mensaje=mensaje)
        else:
            return render_template('puntos/editar_punto.html', punto=punto, mensaje=mensaje, errores=errores)
    else:
        return render_template('puntos/editar_punto.html', punto=punto, mensaje=mensaje)
        

def publicar(id):
    permisos.validar_permisos('punto_encuentro_update')
    PuntoEncuentro.publicar_punto(id)
    return redirect(url_for('administrar_puntos'))

def despublicar(id):
    permisos.validar_permisos('punto_encuentro_update')
    PuntoEncuentro.despublicar_punto(id)
    return redirect(url_for('administrar_puntos'))

def borrar_punto(id):
    permisos.validar_permisos('punto_encuentro_destroy')
    PuntoEncuentro.borrar_punto(id)
    return redirect(url_for('administrar_puntos'))