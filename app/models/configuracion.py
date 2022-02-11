from app.db import db


class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    cantidad_elementos_pagina = db.Column(db.Integer)
    criterio_ordenacion = db.Column(db.String(15))
    color_primario = db.Column(db.String(20))
    color_secundario = db.Column(db.String(20))
    color_terciario = db.Column(db.String(20))


    def __init__(self, cantidad, criterio, color_primario, color_secundario, color_terciario):
        self.cantidad_elementos_pagina = cantidad
        self.criterio_ordenacion = criterio
        self.color_primario = color_primario
        self.color_Secundario = color_secundario
        self.color_terciario = color_terciario

    
    @classmethod
    def todo(cls):
        return cls.query.all()

    
    @classmethod
    def obtener_configuracion(cls):
        return cls.query.filter_by(id=1).first()

    
    @classmethod
    def editar(cls, cantidad, criterio, color_primario, color_secundario, color_terciario):
        datos = cls.obtener_configuracion()
        datos.cantidad_elementos_pagina = cantidad
        datos.criterio_ordenacion = criterio
        datos.color_primario = color_primario
        datos.color_secundario = color_secundario
        datos.color_terciario = color_terciario
        db.session.commit()
        return datos
