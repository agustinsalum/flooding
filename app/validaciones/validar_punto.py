


from app.models.punto_encuentro import PuntoEncuentro

"""manejo de errores del lado del servidor"""
class ValidarPunto(PuntoEncuentro):

    # Constructores y comienzo

    def __init__(self, parametros):
        self.errors = {}
        self.parametros = parametros
    
    
    def validar(self):
        # El nombre y la direccion son obligatorios
        self.__validar_nombre()
        self.__validar_direccion()
        self.__validar_email()
        self.__validar_punto()
        return self.errors

    # Getters

    def nombre_punto(self):
        return self.parametros["nombre"]
    
    def direccion_punto(self):
        return self.parametros["direccion"]
    
    def correo_punto(self):
        return self.parametros["email"]
    
    def latitud_punto(self):
        return self.parametros["latitud"]
    
    def longitud_punto(self):
        return self.parametros["longitud"]
    
    # Validaciones

    def no_ingreso_nombre(self):
        return not self.nombre_punto()
    
    def no_ingreso_direccion(self):
        return not self.direccion_punto()
    
    def existe_nombre(self):
        return self.query.filter_by(nombre=self.nombre_punto()).first()
    
    
    def existe_email(self):
         return self.query.filter_by(email=self.correo_punto()).first()

    
    
    def ingreso_valores_mapa(self):
        return len(self.latitud_punto()) == 0 and len(self.longitud_punto()) == 0
    

    # Metodos principales que llaman a las validaciones
        

    
    def __validar_nombre(self):
        if self.no_ingreso_nombre():
            self.errors['Error por faltante de nombre'] = "No ingreso nombre"
        else:
            if self.existe_nombre():
                self.errors['Error por nombre repetido'] = "Ya existe un punto con ese nombre"
    
    def __validar_direccion(self):
        if self.no_ingreso_direccion():
            self.errors['Error con la direccion'] = "No ingreso la direccion"
    
    def __validar_email(self):
        if self.existe_email():
            self.errors['Error con el correo'] = "El correo ya existe"
    
    
    def __validar_punto(self):
        if self.ingreso_valores_mapa():
            self.errors['Error en el mapa'] = "Debe ingresar un punto en el mapa"

