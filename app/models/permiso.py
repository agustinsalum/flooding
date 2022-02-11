from app.db import db

class Permiso(db.Model):
    __tablename__= 'permiso'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40))

    
    def __init__(self, nombre):
        self.nombre = nombre

    
    @classmethod
    def todo(cls):
        return cls.query.all()
        
    
    @classmethod
    def obtener_por_nombre(cls,nombre_permiso):
        # Dado el nombre obtenemos la instancia
        return cls.query.filter_by(nombre=nombre_permiso).first()
    
