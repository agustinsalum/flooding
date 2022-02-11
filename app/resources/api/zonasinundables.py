from flask import jsonify, request
from app.models.zona import Zona
import json

def mostrar_zona(id):
    try:
        zona = Zona.query.get(id)
    except:
        return jsonify({"error": "500 Internal server Error"}), 500
    if not zona:
        return jsonify({"error": "404 Not Found"}), 404
    array = []
    array2 = json.loads(zona.coordenadas)
    for coordenadas in array2:
        dicCoords = { "lat" : coordenadas[0] , "long": coordenadas[1]}
        array.append(dicCoords)
    dic= { "id" : zona.id,
           "nombre": zona.nombre,
           "estado": zona.estado,
           "color": zona.color,
           "coords": array
         }
    resp= {'atributos':dic}
    return jsonify(resp), 200

def mostrar_zonas(page=1, size=3, name=''):
    if len(request.args) > 0 :
        if request.args.get('page') != None:
            page = request.args.get('page')
        if request.args.get('size') != None:
            size = request.args.get('size')
        if request.args.get('name') != None:
            name = request.args.get('name')
    if name == '':
        zonas = Zona.obtener_activos().paginate(int(page), per_page=int(size))
    else:
        z = Zona.filtrar_por_nombre(name).first()
        print('zona')
        print(z)
        if z:
            zonas = Zona.filtrar_por_nombre(name).paginate(int(page), per_page=int(size))
            print(zonas.items)
        else:
            error = 'No existen zonas que contengan esos caracteres'
            return jsonify({"ok": 'false', "error": error }), 200
    lista = []
    for zona in zonas.items:
        array = []
        array2 = json.loads(zona.coordenadas)
        for coordenadas in array2:
            dicCoords = { "lat" : coordenadas[0] , "long": coordenadas[1]}
            array.append(dicCoords)
        dic= { 
                "id" : zona.id,
                "nombre": zona.nombre,
                "estado": zona.estado,
                "color": zona.color,
                "coords":  array
             }
        lista.append(dic)
    resp= {'data': lista, 'totalItems': zonas.total, 'pagina': page, "ok": 'true'}
    response = jsonify(resp)

    return response, 200