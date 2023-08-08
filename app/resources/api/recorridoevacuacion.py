from flask import jsonify, request
from app.models.recorrido import Recorrido
import json

def mostrar_recorrido(id):
    try:
        recorrido = Recorrido.query.get(id)
        print(recorrido.estado)
    except:
        return jsonify({"error": "500 Internal server Error"}), 500
    
    if not recorrido:
        return jsonify({"error": "404 Not Found"}), 404
    array = []
    array2 = json.loads(recorrido.coordenadas)
    for coordenadas in array2:
        dicCoords = { "lat" : coordenadas[0] , "long": coordenadas[1]}
        array.append(dicCoords)

    dic= { "id" : recorrido.id_recorrido,
           "nombre": recorrido.nombre,
           "estado": recorrido.estado,
           "descripcion": recorrido.descripcion, 
           "coordenadas": recorrido.coordenadas
         }
    resp= {'atributos':dic}
    return jsonify(resp), 200


def mostrar_recorridos(page=1, size=3, name=''):
    if len(request.args) > 0 :
        if request.args.get('page') != None:
            page = request.args.get('page')
        if request.args.get('size') != None:
            size = request.args.get('size')
        if request.args.get('name') != None:
            name = request.args.get('name')
    if name == '':
     recorridos = Recorrido.obtener_activos().paginate(per_page=int(size))
    else:
        r = Recorrido.filtrar_por_nombre(name).first()
        # print('recorrido')
        # print(r)
        if r:
            recorridos = Recorrido.filtrar_por_nombre(name).paginate(per_page=int(size))
            # print(recorridos.items)
        else:
            error = 'No existen recorridos que contengan esos caracteres'
            return jsonify({"ok": 'false', "error": error }), 200
    lista = []

    for recorrido in recorridos.items:
        array = []
        array2 = json.loads(recorrido.coordenadas)
        for coordenadas in array2:
            dicCoords = { "lat" : coordenadas[0] , "long": coordenadas[1]}
            array.append(dicCoords)
            dic= { 
                    "id" : recorrido.id_recorrido,
                    "nombre": recorrido.nombre,
                    "descripcion": recorrido.descripcion, 
                    "estado": recorrido.estado,
                    "coordenadas": array
                 }
        lista.append(dic)
    resp= {'data': lista, 'totalItems': recorridos.total, 'pagina': page, "ok": 'true'}
    return jsonify(resp), 200