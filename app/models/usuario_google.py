from app.db import db
from datetime import datetime

from app.models.rol import Rol

roles = db.Table('usuario_google_tiene_rol',
                 db.Column('usuario_id', db.Integer, db.ForeignKey(
                     'usuario_google.id')),
                 db.Column('rol_id', db.Integer, db.ForeignKey(
                     'rol.id')),
                     #extend_existing=True
)

class UsuarioGoogle(db.Model):
    __tablename__ = 'usuario_google'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(30))
    nombre = db.Column(db.String(40))
    apellido = db.Column(db.String(40))
    email = db.Column(db.String(60))
    aprobado = db.Column(db.Integer)
    fecha_solicitud = db.Column(db.Date)
    roles = db.relationship('Rol', secondary=roles, backref=db.backref('usuarios_google_con_el_rol', lazy=True), lazy='subquery')


    @classmethod
    def todo(cls):
        return cls.query.all()
    

    @classmethod
    def obtener_por_id(cls,id):
        # Dado el id obtenemos la instancia
        return cls.query.get(id)


    @classmethod
    def existe_correo(cls,correo):
        return cls.query.filter_by(email=correo).first()
    

    @classmethod
    def esta_aprobado(cls,id):
        datos = cls.query.filter_by(id=id).first()
        return datos.aprobado
    

    @classmethod
    def crear_pendiete(cls,nombre_usuario, nombre, apellido, email):
        # Obtenemos solo la fecha sin la hora-minutos-segundos
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        nuevo_usuario = cls(usuario=nombre_usuario, nombre=nombre, apellido=apellido, email=email, aprobado=False, fecha_solicitud=fecha_hoy)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return True
    

    # Metodo de clase llamado por el usuario
    def tiene_permiso(self, nombre_permiso):
        res = False
        for rol in self.roles:
            for permiso in rol.permisos:
                if permiso.nombre == nombre_permiso:
                    res = True
        return res
    
    
    @classmethod
    def aprobar(cls, id, roles):
        lista_roles = []
        for rol in roles:
            lista_roles.append(Rol.query.filter_by(id = rol).first())
        datos = cls.query.filter_by(id=id).first()
        datos.aprobado = 1
        datos.roles = lista_roles
        db.session.commit()
        return datos


