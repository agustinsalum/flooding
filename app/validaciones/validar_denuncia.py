
from app.models.denuncia import Denuncia

"""manejo de errores del lado del servidor"""
class ValidarDenuncia(Denuncia):

    # Constructores y comienzo

    def __init__(self, parametros):
        self.errors = {}
        self.parametros = parametros
    
    
    def validar(self):
        # El titulo, la categoria, la descripcion y todos los datos del denunciante son obligatorios
        self.__validar_titulo()
        self.__validar_categoria()
        self.__validar_descripcion()
        self.__validar_datos_denunciante()
        self.__validar_puntos()
        return self.errors

    # Getters

    def titulo_denuncia(self):
        return self.parametros["titulo"]
    
    def categoria_denuncia(self):
        return self.parametros["categoria"]
    
    def descripcion_denuncia(self):
        return self.parametros["descripcion"]
    
    def latitud_denuncia(self):
        return self.parametros["latitud"]
    
    def longitud_denuncia(self):
        return self.parametros["longitud"]
    
    def nombre_denuncia(self):
        return self.parametros["nombre"]
    
    def apellido_denuncia(self):
        return self.parametros["apellido"]
    
    def telefono_denuncia(self):
        return self.parametros["telefono"]
    
    def email_denuncia(self):
        return self.parametros["email"]
    
    # Validaciones
    
    
    def existe_titulo(self):
        return self.query.filter_by(titulo=self.titulo_denuncia()).first()
    
    def no_ingreso_titulo(self):
        return not self.titulo_denuncia()
    
    def no_ingreso_categoria(self):
        return not self.categoria_denuncia()
    
    def no_ingreso_descripcion(self):
        return not self.descripcion_denuncia()
    
    def no_ingreso_datos_denunciante(self):
        return not self.nombre_denuncia() or not self.apellido_denuncia() or not self.telefono_denuncia() or not self.email_denuncia()
    
    def ingreso_valores_mapa(self):
        return len(self.latitud_denuncia()) == 0 and len(self.longitud_denuncia()) == 0
    

    # Metodos principales que llaman a las validaciones
        

    
    def __validar_titulo(self):
        if self.no_ingreso_titulo():
            self.errors['Error por faltante de titulo'] = "No ingreso un titulo"
        else:
            if self.existe_titulo():
                self.errors['Error por titulo repetido'] = "Ya existe un titulo con ese nombre"
    
    def __validar_categoria(self):
        if self.no_ingreso_categoria():
            self.errors['Error con la categoria'] = "No ingreso una categoria"
    
    def __validar_descripcion(self):
        if self.no_ingreso_descripcion():
            self.errors['Error con la descripcion'] = "No ingreso una descripcion"
    
    def __validar_datos_denunciante(self):
        if self.no_ingreso_datos_denunciante():
            self.errors['Error con los datos del denunciante'] = "Faltan datos del denunciante"
    
    
    def __validar_puntos(self):
        if self.ingreso_valores_mapa():
            self.errors['Error en el mapa'] = "Debe ingresar un punto en el mapa"