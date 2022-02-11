
from app.models.configuracion import Configuracion

"""manejo de errores del lado del servidor"""
class ValidarConfiguracion(Configuracion):

    # Constructores y comienzo

    def __init__(self, parametros):
        self.errors = {}
        self.parametros = parametros
    
    
    def validar(self):
        self.__validar_cantidad_paginas()
        return self.errors
    

     # Validaciones
    
    def falta_cantidad_paginas(self):
        return not self.parametros["cantPagina"]
    
    def cantidad_paginas_cero(self):
        cantidad_paginas = int(self.parametros["cantPagina"])
        return cantidad_paginas < 1
    
    

    # Metodos principales que llaman a las validaciones
    
    def __validar_cantidad_paginas(self):
        if self.falta_cantidad_paginas():
            self.errors['Cantida de paginas'] = "debe ingresar la cantidad de paginas"
        else:
            if self.cantidad_paginas_cero():
                self.errors['Cantida de paginas'] = "La cantidad de paginas debe ser mayor o igual a 1"