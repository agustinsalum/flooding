from app.models.usuario_google import UsuarioGoogle


class ValidarUsuarioGoogle(UsuarioGoogle):

    # Constructores y comienzo

    def __init__(self, nombre_usuario,correo):
        self.errors = {}
        self.nombre_usuario = nombre_usuario
        self.correo = correo 
    
    
    def validar(self):
        self.__validar_nombre_usuario()
        self.__validar_email()
        return self.errors

    # Getters

    def nombre_usuario_google(self):
        return self.nombre_usuario
    
    def email_user_google(self):
        return self.correo

    # Validaciones
    
    def existe_usuario(self):
        return self.query.filter_by(usuario=self.nombre_usuario_google()).first()
    
    def existe_email(self):
        return self.query.filter_by(email=self.email_user_google).first()


    # Metodos principales que llaman a las validaciones
        

    
    def __validar_nombre_usuario(self):
        if self.existe_usuario():
            self.errors['Error con el usuario'] = "Ya existe el nombre de usuario"
    
    
    def __validar_email(self):
        if self.existe_email():
            self.errors['Error con el mail'] = "Ya existe el mail registrado"

