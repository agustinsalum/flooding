from flask import render_template, url_for, request, redirect, session
from app.helpers import permisos
from app.models.denuncia import Denuncia
from app.models.denuncia_categoria import DenunciaCategoria
from app.models.denuncia_estado import DenunciaEstado
from app.models.usuario import Usuario
from app.validaciones.validar_denuncia import ValidarDenuncia
from app.models.configuracion import Configuracion
from app.models.seguimiento import Seguimiento


def denuncia():
    permisos.validar_permisos('denuncia_index')
    return render_template('denuncia/denuncias.html')

def crear_denuncia():
    permisos.validar_permisos('denuncia_create')
    categorias= DenunciaCategoria.todo()
    usuarios = Usuario.todo()
    if request.method == 'POST':
        datos_denuncia = request.form
        mensaje = ''
        errores = ValidarDenuncia(datos_denuncia).validar()
        if not errores:
            Denuncia.crear(datos_denuncia['titulo'],
                datos_denuncia['descripcion'],
                datos_denuncia['latitud'],
                datos_denuncia['longitud'],
                datos_denuncia['apellido'],
                datos_denuncia['nombre'],
                datos_denuncia['telefono'],
                datos_denuncia['email'],
                datos_denuncia['usuario'],
                datos_denuncia['categoria'])
            mensaje = "Denuncia creada exitosamente"
            return render_template('denuncia/crear_denuncia.html', categorias=categorias, usuarios=usuarios, mensaje = mensaje)
        else:
            return render_template('denuncia/crear_denuncia.html', categorias=categorias, usuarios=usuarios, errores=errores)
    else:
        # Primero entra aca
        return render_template('denuncia/crear_denuncia.html', categorias=categorias, usuarios=usuarios)


def listado(titulo=' ', estado='todas', page=1, fecha_desde='dd/mm/aaaa', fecha_hasta='dd/mm/aaaa'):
    permisos.validar_permisos('denuncia_index')
    per_page = Configuracion.obtener_configuracion().cantidad_elementos_pagina
    denuncias = Denuncia.todo()
    if (not denuncias):
        mensaje_sin_denuncias = "No existen denuncias cargadas en este momento"
        return render_template("denuncia/listado.html", denuncias=denuncias, mensaje_sin_denuncias=mensaje_sin_denuncias)
    denuncias = denuncias[0]
    if request.method == 'GET':
        if request.args:
            params = request.args
            if params['estado']:
                estado_alternativo= params['estado']
            else:
                estado_alternativo = estado
            if params['titulo']:
                estado_alternativo= params['titulo']
            else:
                estado_alternativo = titulo
            if params['fecha_desde']:
                fecha_desde_alternativo= params['fecha_desde']
            else:
                fecha_desde_alternativo = fecha_desde
            if params['fecha_hasta']:
                fecha_hasta_alternativo= params['fecha_hasta']
            else:
                fecha_hasta_alternativo = fecha_hasta
        else:
            estado_alternativo = estado
            titulo_alternativo = titulo
            fecha_desde_alternativo = fecha_desde
            fecha_hasta_alternativo = fecha_hasta
    if request.method == 'POST':
        page=1
        params = request.form
        titulo_alternativo = params['titulo']
        estado_alternativo = params['estado']
        fecha_desde_alternativo = params['fecha_desde']
        if(fecha_desde_alternativo==''):
            fecha_desde_alternativo = 'dd/mm/aaaa'
        fecha_hasta_alternativo = params['fecha_hasta']
        if(fecha_hasta_alternativo == ''):
            fecha_hasta_alternativo = 'dd/mm/aaaa'
    orden = Configuracion.obtener_configuracion().criterio_ordenacion
    if orden == 'desc': 
        denuncias = denuncias.query.order_by(Denuncia.titulo.desc())
    else:
        denuncias = denuncias.query.order_by(Denuncia.titulo.asc())
    if titulo_alternativo != ' ':
        denuncias = denuncias.filter(Denuncia.titulo.like('%' + titulo_alternativo + '%'))
    if estado_alternativo != 'todas':        
        denuncias = denuncias.filter_by(estado_id = estado_alternativo) 
    if (fecha_desde_alternativo != 'dd/mm/aaaa' or fecha_hasta_alternativo != 'dd/mm/aaaa'):         
        denuncias = denuncias.filter(Denuncia.fecha_creacion.between(fecha_desde_alternativo, fecha_hasta_alternativo))        
    denuncias = denuncias.paginate(per_page=per_page)
    return render_template("denuncia/listado.html", denuncias=denuncias, titulo = titulo_alternativo, estado = estado_alternativo, fecha_desde = fecha_desde_alternativo, fecha_hasta = fecha_hasta_alternativo)
    
#Edicion de un usuario seleccionado en la lista
def editar_denuncia(id):
    permisos.validar_permisos('denuncia_update')
    denuncia = Denuncia.obtener_por_id(id)
    categorias= DenunciaCategoria.todo()  
    estados = DenunciaEstado.todo()
    usuarios = Usuario.todo()  
    mensaje = ''
    if request.method == 'POST':
        datos_nuevos_denuncia = request.form        
        mensaje = ''
        errores = ValidarDenuncia(datos_nuevos_denuncia).validar()
        # Si no modifico su titulo eliminamos ese error
        if denuncia.titulo == datos_nuevos_denuncia['titulo']:
            del errores["Error por titulo repetido"]
        if not errores:
            Denuncia.editar(id, datos_nuevos_denuncia['titulo'],
                datos_nuevos_denuncia['categoria'],
                datos_nuevos_denuncia['descripcion'],
                datos_nuevos_denuncia['latitud'],
                datos_nuevos_denuncia['longitud'],
                datos_nuevos_denuncia['usuario'],
                datos_nuevos_denuncia['apellido'],
                datos_nuevos_denuncia['nombre'],
                datos_nuevos_denuncia['telefono'],
                datos_nuevos_denuncia['email'])
            mensaje = "Denuncia editada exitosamente"                                               
            return render_template('denuncia/editar_denuncia.html', denuncia=denuncia, categorias=categorias, mensaje=mensaje,estados=estados, usuarios=usuarios)
        else:
            return render_template('denuncia/editar_denuncia.html', denuncia=denuncia, categorias=categorias, errores=errores,estados=estados, usuarios=usuarios)

    else:
        return render_template('denuncia/editar_denuncia.html', denuncia=denuncia,categorias=categorias, mensaje=mensaje,estados=estados, usuarios=usuarios)

def borrar_denuncia(id):
    permisos.validar_permisos('denuncia_destroy')
    Denuncia.borrar_denuncia(id)
    return redirect(url_for('denuncias'))


def listado_seguimiento(titulo=' ', page=1):
    permisos.validar_permisos('denuncia_show')
    per_page = Configuracion.obtener_configuracion().cantidad_elementos_pagina
    denuncias = Denuncia.todo()
    if (not denuncias):
        mensaje_sin_denuncias = "No existen denuncias cargadas en este momento"
        return render_template("denuncia/listado_seguimiento.html", denuncias=denuncias, mensaje_sin_denuncias=mensaje_sin_denuncias)
    denuncias = denuncias[0]
    if request.method == 'GET':
        if request.args:
            params = request.args            
            if params['titulo']:
                titulo_alternativo= params['titulo']
            else:
                titulo_alternativo = titulo
        else:            
            titulo_alternativo = titulo            
    if request.method == 'POST':
        page=1
        params = request.form
        titulo_alternativo = params['titulo']
    orden = Configuracion.obtener_configuracion().criterio_ordenacion
    if orden == 'desc': 
        denuncias = denuncias.query.order_by(Denuncia.titulo.desc())
    else:
        denuncias = denuncias.query.order_by(Denuncia.titulo.asc())
    if titulo_alternativo != ' ':
        denuncias = denuncias.filter(Denuncia.titulo.like('%' + titulo_alternativo + '%'))
    denuncias = denuncias.paginate(per_page=per_page)
    return render_template("denuncia/listado_seguimiento.html", denuncias=denuncias, titulo = titulo_alternativo)    

def validar_denuncia(id):
    permisos.validar_permisos('denuncia_update')   
    denuncia = Denuncia.obtener_por_id(id) 
    estados = DenunciaEstado.todo()         
    categorias= DenunciaCategoria.todo()          
    seguimientos= Seguimiento.todo() 
    usuarios = Usuario.todo()     
    mensaje = ''                                            
    if request.method == 'POST':
        datos_denuncia = request.form        
        if datos_denuncia['estado'] == "Cerrada":              
            texto_seguimiento = 'No fue posible contactar al denunciante'
        else: 
            texto_seguimiento =  datos_denuncia['descripcionseguimiento']                   
        Denuncia.validar_denuncia(id, datos_denuncia['estado'] ,texto_seguimiento, session["usuario"].id)
        mensaje = "Seguimiento agregado exitosamente"                                              
        return render_template('denuncia/validar_denuncia.html', denuncia=denuncia, categorias=categorias, mensaje=mensaje,estados=estados, usuarios=usuarios, seguimientos=seguimientos)        
    else:
        return render_template('denuncia/validar_denuncia.html', denuncia=denuncia,categorias=categorias, mensaje=mensaje,estados=estados, usuarios=usuarios, seguimientos=seguimientos)

def asignarme_denuncia(id):    
    permisos.validar_permisos('denuncia_update')    
    Denuncia.asignarme_denuncia(id, session["usuario"].id)
    return redirect(url_for('listado_seguimiento'))

def asignar_denuncia_usuario(id):
    permisos.validar_permisos('denuncia_update')    
    denuncia = Denuncia.obtener_por_id(id) 
    usuarios = Usuario.todo()
    categorias= DenunciaCategoria.todo()         
    mensaje = ''  
    if request.method == 'POST':   
        d = request.form
        Denuncia.asignar_denuncia_usuario(id, d['usuarioAsignadoNuevo'])
        mensaje = "Usuario asignado exitosamente"                                              
    return render_template('denuncia/asignar_denuncia_usuario.html', denuncia=denuncia, mensaje=mensaje, usuarios=usuarios,categorias=categorias)        
    