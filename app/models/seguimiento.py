
from app.db import db
from datetime import datetime

class Seguimiento(db.Model):
    __tablename__ = 'seguimiento'
    id_seguimiento = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text)
    autor_ide = db.Column("autor",db.Integer, db.ForeignKey('usuario.id'))
    autor = db.relationship("Usuario", backref="usuarioss")
    fecha = db.Column(db.Date)    
    denuncia_id = db.Column("denuncia",db.Integer, db.ForeignKey('denuncia.id_denuncia'))
    denuncia = db.relationship("Denuncia", backref="seguimientos")
    estado_id = db.Column("estado",db.Integer, db.ForeignKey('denuncia_estado.id_estado'))
    estado = db.relationship("DenunciaEstado", backref="estadoss")

    
    @classmethod
    def todo(cls):
        return cls.query.all()
        
    
    @classmethod
    def crear(cls, descripcion_seguimiento, id_denuncia, usuario,estado):
        fecha_actual = datetime.now()
        nuevo_seguimiento = cls(descripcion=descripcion_seguimiento, autor_ide=usuario, fecha=fecha_actual, denuncia_id=id_denuncia, estado_id = estado)
        db.session.add(nuevo_seguimiento)
        db.session.commit()
        return nuevo_seguimiento