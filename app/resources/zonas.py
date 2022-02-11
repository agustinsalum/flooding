import csv 
import io
import json
from flask import render_template, request, Markup
from app.helpers import permisos
from app.models.configuracion import Configuracion
from app.models.zona import Zona
from app.validaciones.validar_zona import ValidarZona

def index(nombre=' ', estado="todos", page=1, mensaje = None):
  permisos.validar_permisos('zonas_index')
  per_page = Configuracion.obtener_configuracion().cantidad_elementos_pagina
  zonas = Zona.todo()
  if zonas:
    zonas = zonas[0]
  else:
    return render_template("zonas/index.html", mensaje='Aún no existen zonas en tu base de datos')
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
            if params['page']:
                page= int(params['page'])
            else:
                page = 1
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
      zonas = zonas.query.order_by(Zona.nombre.desc())
  else:
      zonas = zonas.query.order_by(Zona.nombre.asc())

  if nombre_alternativo != ' ':
      zonas = zonas.filter(Zona.nombre.like('%' + nombre_alternativo + '%'))
  if estado_alternativo != 'todos':
      zonas = zonas.filter_by(estado = estado_alternativo)
  zonas = zonas.paginate(page, per_page=per_page)

  return render_template("zonas/index.html", zonas=zonas, nombre = nombre_alternativo, estado = estado_alternativo, mensaje= mensaje)


def activar(id):
    permisos.validar_permisos('zonas_import')
    zona = Zona.activar_zona(id)
    if zona.estado == 1:
        return index(mensaje='Se ha activado la zona ' + zona.nombre)

def desactivar(id):
    permisos.validar_permisos('zonas_destroy')
    zona = Zona.desactivar_zona(id)
    if zona.estado == 0:
        return index(mensaje='Se ha desactivado la zona ' + zona.nombre)

def eliminar(id):
    permisos.validar_permisos('zonas_destroy')
    zona = Zona.eliminar_zona(id)
    return index(mensaje='Se ha eliminado la zona ' + zona.nombre)

def editar_zona(id):
    permisos.validar_permisos('zonas_show')
    if request.method == 'POST':
        datos_nuevos_zona = request.form
        Zona.editar_zona(id, datos_nuevos_zona['color'])            
        zona = Zona.obtener_por_id(id)

        zona1 = json.loads(zona.coordenadas)
        cant = len(zona1)
        return render_template('zonas/editar.html', cant= cant, zona = zona, mensaje='La zona: ' + zona.nombre + ', fue editada exitosamente'   )        
    else:
        zona = Zona.obtener_por_id(id)
        # import pdb; pdb.set_trace()
        zona1 = json.loads(zona.coordenadas)
        cant = len(zona1)
        return render_template('zonas/editar.html', cant= cant, zona = zona )
       
def ver_zona():
    return render_template('zona/index.html')

def upload():
    permisos.validar_permisos('zonas_import')
    if request.method == 'GET':
        return render_template('zonas/import.html')
    elif request.method == 'POST':
        archivo = request.files['file']
        if ValidarZona.no_existe_archivo(archivo):
            return render_template('zonas/import.html', mensaje= 'no subiste ningun archivo')
        try:
            stream = io.StringIO(archivo.stream.read().decode("UTF8"), newline=None)
        except:
            return render_template('zonas/import.html', mensaje= 'el archivo no posee el formato csv correspondiente')
        
        csv_input = csv.reader(stream)
        array = list(csv_input)
        name=-1
        area=-1
        if ValidarZona.no_existe_cabecera(array):
            return render_template('zonas/import.html', mensaje= 'el archivo no posee las cabeceras correspondientes en la fila 1')
        else:
            if (array[0][0] == 'name'):
                name = 0
                if (array[0][1] == 'area'):
                    area= 1
                else:
                    return render_template('zonas/import.html', mensaje= 'el archivo no posse la estructura adecuada name/area')
            else:
                if (array[0][0] == 'area'):
                    area = 0
                    if (array[0][1] == 'name'):
                        name= 1
                    else:
                        return render_template('zonas/import.html', mensaje= 'el archivo no posse la estructura adecuada area/name')
                else:
                    return render_template('zonas/import.html', mensaje= 'el archivo no posse la estructura adecuada: name, area')
        
        print(name, area)
        i=0
        mensaje= Markup('Para cada zona con sus respectivas coordenadas: <br/>')
        for row in array:
            if i != 0:
                # checkear si existe en la bd la zona
                existe = Zona.obtener_por_nombre(row[name])
                print(existe)
                if(existe):
                    # Existe
                    # for x in range(0,len(array)):
                    # print (array[x])
                    mensaje = mensaje + 'Zona ya existente ' + row[name] + ': '
                    # check si es igual
                    coords = Zona.obtener_coordenadas(row[name])
                    if ( coords == row[area] ):
                        mensaje = mensaje + 'posee las mismas coordenadas y no fue actualizado' + Markup('. <br/>')
                    else:
                        Zona.actualizar_coordenadas(row[name],row[area])
                        mensaje = mensaje + 'posee coordenadas distintas y fue actualizado' + Markup('. <br/>')
                else:
                    # No existe
                    if (Zona.crear_zona(row[name], row[area])):
                        mensaje = mensaje + 'Zona ' + row[name] + Markup(': fue agregada correctamente <br/>')
            i = i+1
        return render_template('zonas/import.html', mensaje= Markup('El archivo fue procesado... <br/>') + mensaje)
  
