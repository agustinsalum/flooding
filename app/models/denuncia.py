
from app.db import db
from datetime import datetime
from app.models.denuncia_categoria import DenunciaCategoria
from app.models.denuncia_estado import DenunciaEstado
from app.models.usuario import Usuario
from app.models.seguimiento import Seguimiento


class Denuncia(db.Model):
    __tablename__ = 'denuncia'
    id_denuncia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(40))
    fecha_creacion = db.Column(db.Date)
    fecha_cierre = db.Column(db.Date)
    descripcion = db.Column(db.Text)
    latitud = db.Column(db.Text)
    longitud = db.Column(db.Text)
    apellido = db.Column(db.String(40))
    nombre = db.Column(db.String(40))
    telefono = db.Column(db.String(40))
    email = db.Column(db.String(40))
    # backref nos ahorra hacer la relacion desde la otra clase
    # representa la columna "categoria_id"
    categoria_id = db.Column("categoria",db.Integer, db.ForeignKey('denuncia_categoria.id_categoria'))
    # método disponible SQLAlchemy para traernos las cotegorias relacionadas con la denuncia
    categoria = db.relationship("DenunciaCategoria", backref="denuncias")
    #
    estado_id = db.Column("estado",db.Integer, db.ForeignKey('denuncia_estado.id_estado'))
    estado = db.relationship("DenunciaEstado", backref="estados")
    #
    asignado_id = db.Column("asignado",db.Integer, db.ForeignKey('usuario.id'))
    asignado = db.relationship("Usuario", backref="usuarios")

   
    @classmethod
    def todo(cls):
        return cls.query.all()
    

    @classmethod
    def obtener_por_id(cls,id_denuncia):
        # Dado el id obtenemos la instancia
        return cls.query.get(id_denuncia)
    
    
    def crear_api(titulo, descripcion, latitud, longitud, apellido, nombre, telefono, email, categoria):
        fecha_actual = datetime.now()
        una_categoria = DenunciaCategoria.obtener_por_nombre(categoria)
        # se crea automaticamente con el estado "En curso"
        estado_en_curso = DenunciaEstado.obtener_por_nombre("En curso")
        nueva_denuncia = Denuncia(titulo=titulo, fecha_cierre=None, fecha_creacion=fecha_actual, descripcion=descripcion, latitud=latitud, longitud=longitud, apellido=apellido, nombre=nombre, telefono=telefono, email=email, estado=estado_en_curso, asignado=None, categoria=una_categoria)
        db.session.add(nueva_denuncia)
        db.session.commit()
        return True
  
    
    @classmethod
    def crear(cls, titulo, descripcion, latitud, longitud, apellido, nombre, telefono, email, usuario, categoria):
        fecha_actual = datetime.now()
        # Por el mapeo necesitamos pasarle la instancia completa
        una_categoria = DenunciaCategoria.obtener_por_nombre(categoria)
        # se crea automaticamente con el estado "En curso"
        estado_en_curso = DenunciaEstado.obtener_por_nombre("En curso")
        un_usuario = Usuario.obtener_por_id(usuario)
        nueva_denuncia = cls(titulo=titulo, fecha_cierre=None, fecha_creacion=fecha_actual, descripcion=descripcion, latitud=latitud, longitud=longitud, apellido=apellido, nombre=nombre, telefono=telefono, email=email, estado=estado_en_curso, asignado=un_usuario, categoria=una_categoria)
        db.session.add(nueva_denuncia)
        db.session.commit()
        return True

    
    @classmethod
    def editar(cls,id, titulo, categoria, descripcion, latitud, longitud, usuario, apellido, nombre, telefono, email):                
        datos = cls.query.filter_by(id_denuncia=id).first()
        una_categoria = DenunciaCategoria.obtener_por_nombre(categoria)
        un_usuario = Usuario.obtener_por_id(usuario)
        datos.titulo = titulo
        datos.fecha_cierre = None
        datos.categoria = una_categoria
        datos.descripcion = descripcion
        datos.latitud = latitud
        datos.longitud = longitud
        datos.asignado = un_usuario               
        datos.apellido = apellido
        datos.nombre = nombre
        datos.telefono = telefono
        datos.email = email   
        db.session.commit()
        return datos

    
    @classmethod
    def borrar_denuncia(cls,id):
        datos = cls.query.filter_by(id_denuncia=id).first()
        datos.id_denuncia = id
        db.session.delete(datos)
        db.session.commit()
        return True

    
    @classmethod
    def validar_denuncia(cls, id, estado, texto_seguimiento, id_usuario):                
        datos = cls.obtener_por_id(id)               
        un_estado = DenunciaEstado.obtener_por_nombre(estado)               
        datos.estado = un_estado
        if (un_estado.nombre == 'Cerrada'):
            datos.fecha_cierre = datetime.now()
        nuevo_seguimiento = Seguimiento.crear(texto_seguimiento, id, id_usuario,un_estado.id_estado)
        datos.seguimientos.append(nuevo_seguimiento)
        db.session.add(datos)               
        db.session.commit()
        return datos

    
    @classmethod
    def obtener_cerrados(cls):
        return cls.query.filter_by(estado_id=4)


    @classmethod
    def asignarme_denuncia(cls, id, id_usuario):               
        datos = cls.obtener_por_id(id)
        un_usuario = Usuario.obtener_por_id(id_usuario)
        datos.asignado = un_usuario
        db.session.commit()
        return datos


    @classmethod
    def asignar_denuncia_usuario(cls, id, usuario_asignado_nuevo):                
        datos = cls.obtener_por_id(id)
        un_usuario = Usuario.obtener_por_id(usuario_asignado_nuevo)
        datos.asignado = un_usuario               
        db.session.commit()
        return datos