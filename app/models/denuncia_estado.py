
from app.db import db

class DenunciaEstado(db.Model):
    __tablename__ = 'denuncia_estado'
    id_estado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40))

    
    def __init__(self, id, nombre):
        self.id_estado = id
        self.nombre = nombre

        
    @classmethod
    def todo(cls):
        return cls.query.all()

    
    @classmethod
    def obtener_por_nombre(cls,nombre_estado):
        # Dado el nombre obtenemos la instancia
        return cls.query.filter_by(nombre=nombre_estado).first()
        
    
    @classmethod
    def obtener_por_id(cls,id_estado):
        # Dado el id obtenemos la instancia
        return cls.query.get(id_estado)
