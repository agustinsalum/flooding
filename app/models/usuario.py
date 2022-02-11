
from app.db import db
from datetime import datetime
from app.models.rol import Rol
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph



roles = db.Table('usuario_tiene_rol',
                 db.Column('usuario_id', db.Integer, db.ForeignKey(
                     'usuario.id')),
                 db.Column('rol_id', db.Integer, db.ForeignKey(
                     'rol.id')),
                     #extend_existing=True
)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(20))
    clave = db.Column(db.String(255))
    nombre = db.Column(db.String(40))
    apellido = db.Column(db.String(40))
    email = db.Column(db.String(60))
    activo = db.Column(db.Integer)
    fecha_actualizacion = db.Column(db.Date)
    fecha_creacion = db.Column(db.Date)
    roles = db.relationship('Rol', secondary=roles, backref=db.backref('usuarios_con_el_rol', lazy=True), lazy='subquery')


    @classmethod
    def todo(cls):
        return cls.query.all()
    

    # Metodo de instancia llamado por la clase
    def verificar_clave(self, clave):
     return checkph(self.clave, clave)
    

    @classmethod
    def obtener_por_nombre(cls,nombre_usuario):
        # Dado el nombre obtenemos la instancia
        return cls.query.filter_by(nombre=nombre_usuario).first()


    @classmethod
    def obtener_por_correo(cls, correo):
        return cls.query.filter_by(email=correo).first()
    

    # Metodo de instancia llamado por la instancia
    def tiene_permiso(self, nombre_permiso):
        res = False
        for rol in self.roles:
            for permiso in rol.permisos:
                if permiso.nombre == nombre_permiso:
                    res = True
        return res
    

    @classmethod
    def crear(cls, nombre_usuario, clave_no_encriptada, nombre, apellido, email, roles):
        today = datetime.now()
        #Encriptar contraseña
        clave_encriptada = genph(clave_no_encriptada)
        listaRoles=[]
        for rol in roles:
            listaRoles.append(Rol.query.filter_by(id = rol).first())
        nuevo_usuario = cls(usuario=nombre_usuario, clave=clave_encriptada, nombre=nombre, apellido=apellido, email=email, roles=listaRoles ,activo=True, fecha_actualizacion=today, fecha_creacion=today)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return True


    @classmethod
    def obtener_por_id(cls, id):
        # Dado el id obtenemos la instancia
        return cls.query.get(id)
    

    @classmethod
    def editar(cls, id_usuario, usuario, nombre, apellido, email, roles):        
        lista_roles = []
        for rol in roles:
            lista_roles.append(Rol.query.filter_by(id = rol).first())
        datos = cls.query.filter_by(id=id_usuario).first()
        datos.usuario = usuario
        datos.nombre = nombre
        datos.apellido = apellido
        datos.email = email
        datos.roles = lista_roles
        db.session.commit()
        return datos
    

    @classmethod
    def editar_contraseña(cls, id_usuario, clave):        
        datos = cls.query.filter_by(id=id_usuario).first()
        hash_clave = genph(clave)
        datos.clave = hash_clave
        db.session.commit()
        return datos
    

    @classmethod
    def activar_usuario(cls, id_usuario):
        datos = cls.query.filter_by(id=id_usuario).first()
        datos.activo = 1
        db.session.commit()
        return datos


    @classmethod
    def desactivar_usuario(cls, id_usuario):
        datos = cls.query.filter_by(id=id_usuario).first()
        datos.activo = 0
        db.session.commit()
        return datos