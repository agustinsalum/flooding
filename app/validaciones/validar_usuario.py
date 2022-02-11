
from app.models.usuario import Usuario

"""manejo de errores del lado del servidor"""
class ValidarUsuario(Usuario):

    # Constructores y comienzo

    def __init__(self, parametros):
        self.errors = {}
        self.parametros = parametros
    
    
    def validar(self):
        self.__validar_nombre_usuario()
        self.__validar_email()
        self.__validar_roles()
        return self.errors

    # Getters

    def nombre_usuario_user(self):
        return self.parametros["usuario"]
    
    def email_user(self):
        return self.parametros["email"]
    
    def roles_user(self):
        return self.parametros["roles"]
    
    # Validaciones
    
    def existe_usuario(self):
        return self.query.filter_by(usuario=self.nombre_usuario_user()).first()
    
    def existe_email(self):
        return self.query.filter_by(email=self.email_user()).first()
    
    
    def faltan_roles(self):
        try:
            self.roles_user()
        except KeyError:
            # No envio roles
            return True
        else:
            return False
    

    # Metodos principales que llaman a las validaciones
        

    
    def __validar_nombre_usuario(self):
        if self.existe_usuario():
            self.errors['Error con el usuario'] = "Ya existe el nombre de usuario"
    
    
    def __validar_email(self):
        if self.existe_email():
            self.errors['Error con el mail'] = "Ya existe el mail registrado"
    
    
    def __validar_roles(self):
        if self.faltan_roles():
            self.errors['Error con los roles'] = "Debe ingresar al menos un rol"








