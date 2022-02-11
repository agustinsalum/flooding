from app.db import db
"permiso se usa en la linea 14 como string, para evitar la importacion circular"
from app.models.permiso import Permiso

permisos = db.Table('rol_tiene_permiso',
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permiso.id'), primary_key=True)
)

class Rol(db.Model):
	__tablename__= 'rol'
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(40))
	permisos = db.relationship('Permiso', secondary=permisos, backref=db.backref('roles_con_el_permiso', lazy = True), lazy='subquery')


	def __init__(self, nombre):
		self.nombre = nombre
	

	@classmethod
	def obtener_por_nombre(cls,nombre_rol):
		return cls.query.filter_by(nombre=nombre_rol).first()
	

	@classmethod
	def todo(cls):
		return cls.query.all()
	

	@classmethod
	def crear(cls, nuevo_rol):
		nuevo_rol = cls(nuevo_rol)
		db.session.add(nuevo_rol)
		db.session.commit()
		return nuevo_rol
	
	
	# Metodo de instancia llamado por la instancia rol_admin y rol_operador
	def asignar_permiso(self,nuevo_permiso):
		self.permisos.append(nuevo_permiso)

