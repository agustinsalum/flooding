# Para imprimir y mostrar en formato JSON
from flask import jsonify
from app.models.denuncia import Denuncia
from flask import request
from app.helpers import configuracion_colores


def mostrar_denuncia(id):
    try:
        denuncia = Denuncia.query.get(id)
    except:
        return jsonify({"error": "500 Internal server Error"}), 500
    
    if not denuncia:
        return jsonify({"error": "404 Not Found"}), 404
    
    dic= { "id_denuncia" : denuncia.id_denuncia,
           "titulo": denuncia.titulo,
           "descripcion": denuncia.descripcion, 
           "latitud":denuncia.latitud,
           "longitud": denuncia.longitud,
           "nombre_denunciante": denuncia.nombre,
           "telcel_denunciante": denuncia.telefono,

         }
    
    resp= {'atributos':dic}
    return jsonify(resp), 200

#https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination
# Muestra todas las denuncias cerradas
def mostrar_denuncias(page=1):
    totalelementos= configuracion_colores.obtener_configuracion().cantidad_elementos_pagina
    denuncias = Denuncia.obtener_cerrados().paginate(per_page=totalelementos)
    lista = []
    for denuncia in denuncias.items:
        dic= { "id_denuncia" : denuncia.id_denuncia,
                "titulo": denuncia.titulo,
                "descripcion": denuncia.descripcion,
                "latitud":denuncia.latitud,
                "longitud": denuncia.longitud,
                "nombre_denunciante": denuncia.nombre,
                "apellido_denunciante": denuncia.apellido,
                "telcel_denunciante": denuncia.telefono,
                "fecha_de_creacion": str(denuncia.fecha_creacion),
                "fecha_de_cierre": str(denuncia.fecha_cierre),
                "estado": denuncia.estado.nombre
             }
        lista.append(dic)
    resp= {'denuncias': lista, 'total': denuncias.total, 'pagina': page}
    return jsonify(resp), 200


def es_vacio(dato):
    # Retorna verdadero si dato es vacio
    return not bool(dato)

def descripcion_incorrecta(descripcion):
    return len(descripcion) > 600

def correo_incorrecto(correo):
    return not ("@" in correo and '.' in correo)

def telefono_incorrecto(telefono):
    # isdigit() devuelve verdadero si la cadena se compone solo de numeros
    return len(telefono) < 5 or len(telefono) > 11 or ( not telefono.isdigit())   


# 201 Creado                - Indica que la solicitud se ha realizado correctamente y, como resultado, se ha creado un nuevo recurso.
# 400 Petición Incorrecta   - El servidor no pudo entender la solicitud debido a una sintaxis incorrecta.
# 422 Entidad no procesable - El servidor comprende el tipo de contenido y la sintaxis de la entidad de solicitud, pero no se pudo seguir debido a errores de semántica.

def crear_denuncia():
    try:
        if request.method == "POST" :
            result = request.json
            mensaje_error = ""
            mensajes_vacios = [
                " Titulo: Este campo es obligatorio",
                " Categoría: Campo obligatorio",
                " Descripcion: Este campo es obligatorio",
                " Latitud: Este campo es obligatorio",
                " Longitud: Este campo es obligatorio",
                " Apellido: Este campo es obligatorio,",
                " Email: Este campo es obligatorio",
                " Nombre: Este campo es obligatorio",
                " Telefono: Este campo es obligatorio",
                " Nombre: Este campo es obligatorio" ,
                " Categoria: Este campo es obligatorio"
            ]
            mensajes_sintaxis = [
                "Descripcion: La descripcion debe ser menor a 600 caracteres",
                "Email: El correo tiene un formato incorrecto",
                "Telefono: El telefono tiene un formato incorrecto"
            ]
            # El método Enumerate() agrega un contador a un iterable
            # Verificamos vacios
            for posicion, mensaje in enumerate(result):
                if es_vacio(result[mensaje]):
                    mensaje_error = mensaje_error + "\n " + mensajes_vacios[posicion]
            # Verificamos otros errores
            if descripcion_incorrecta(result['descripcion']):
                mensaje_error = mensaje_error + "\n " + mensajes_sintaxis[0]
            if correo_incorrecto(result['email']):
                mensaje_error = mensaje_error + "\n " + mensajes_sintaxis[1]
            if telefono_incorrecto(result['telefono']):
                mensaje_error = mensaje_error + "\n " + mensajes_sintaxis[2]
            if mensaje_error:
                return jsonify({"Error" : mensaje_error}), 400
            Denuncia.crear_api(
                result['titulo'],
                result['descripcion'],
                result['latitud'],
                result['longitud'],
                result['apellido'],
                result['nombre'],
                result['telefono'],
                result['email'],
                result['categoria'])
            dic = { "atributos" : result }
            print (dic)
            return jsonify(dic), 201
    except:
        return jsonify({"error": "422 Entidad no procesable"}), 422
        

