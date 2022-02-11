
from app.models.recorrido import Recorrido
import json
from json.decoder import JSONDecodeError

"""manejo de errores del lado del servidor"""
class ValidarRecorrido(Recorrido):

    # Constructores y comienzo

    def __init__(self, parametros):
        self.errors = {}
        self.parametros = parametros
    
    
    def validar(self):
        # El nombre es obligatorio
        self.__validar_nombre()
        self.__validar_punto()
        return self.errors

    # Getters

    def nombre_recorrido(self):
        return self.parametros["nombre"]
    
    def coordenadas_recorrido(self):
        return self.parametros["arreglo_coordenadas"]
    
    # Validaciones
    
    
    def existe_nombre(self):
        return self.query.filter_by(nombre=self.nombre_recorrido()).first()
    
    def no_ingreso_nombre(self):
        return not self.nombre_recorrido()

    
    def ingreso_valores_mapa(self):
        try:
            zona1 = json.loads(self.coordenadas_recorrido())
            return (len(zona1)) < 3
        except (JSONDecodeError):
            return True

    # Metodos principales que llaman a las validaciones
    
    def __validar_nombre(self):
        if self.no_ingreso_nombre():
            self.errors['Error con el nombre'] = "No ingreso el nombre"
        else:
            if self.existe_nombre():
                self.errors['Error con el nombre'] = "Ya existe un recorrido con ese nombre"
    
    def __validar_punto(self):
        if self.ingreso_valores_mapa():
            self.errors['Error en el mapa'] = "Debe ingresar como minimo 3 puntos en el mapa"