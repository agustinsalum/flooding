from flask import jsonify, request
from app.models.punto_encuentro import PuntoEncuentro

def mostrar_punto(id):
    try:
        punto = PuntoEncuentro.query.get(id)
    except:
        return jsonify({"error": "500 Internal server Error"}), 500
    
    if not punto:
        return jsonify({"error": "404 Not Found"}), 404
    
    dic= { "id" : punto.id_punto,
           "nombre": punto.nombre,
           "direccion": punto.direccion, 
           "lat":punto.latitud,
           "long": punto.longitud,
           "telefono": punto.telefono,
           "email": punto.email
         }
    
    resp= {'atributos':dic }
    return jsonify(resp), 200


def mostrar_puntos(page=1, size=3, name=''):
    if len(request.args) > 0 :
        if request.args.get('page') != None:
            page = request.args.get('page')
        if request.args.get('size') != None:
            size = request.args.get('size')
        if request.args.get('name') != None:
            name = request.args.get('name')
    if name == '':
     puntos = PuntoEncuentro.obtener_activos().paginate(per_page=int(size))
    else:
        p = PuntoEncuentro.filtrar_por_nombre(name).first()
        print('punto')
        print(p)
        if p:
            puntos = PuntoEncuentro.filtrar_por_nombre(name).paginate(per_page=int(size))
            print(puntos.items)
        else:
            error = 'No existen puntos que contengan esos caracteres'
            return jsonify({"ok": 'false', "error": error }), 200
    lista = []
    for punto in puntos.items:
        dic= { "id" : punto.id_punto,
           "nombre": punto.nombre,
           "direccion": punto.direccion, 
           "lat":punto.latitud,
           "long": punto.longitud,
           "telefono": punto.telefono,
           "email": punto.email
         }
        lista.append(dic)
    resp= {'data': lista, 'totalItems': puntos.total, 'pagina': page,  "ok": 'true'}
    return jsonify(resp), 200

