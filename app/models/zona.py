from app.db import db
import random

class Zona(db.Model):
  __tablename__ = 'zona'
  id = db.Column(db.Integer, primary_key=True)
  coordenadas = db.Column(db.Text)
  nombre = db.Column(db.String(40))
  estado = db.Column(db.Integer)
  color = db.Column(db.String(20))
  

  @classmethod
  def todo(cls):
    return cls.query.all()
  

  @classmethod
  def obtener_por_nombre(cls,nombre_zona):
    # Dado el nombre obtenemos la instancia
    return cls.query.filter_by(nombre=nombre_zona).first()
  

  @classmethod
  def filtrar_por_nombre(cls,name):
    return cls.query.filter(Zona.nombre.contains(name))


  @classmethod
  def obtener_por_id(cls, id):
     # Dado el id obtenemos la instancia
    return cls.query.filter_by(id=id).first()
  

  @classmethod
  def crear_zona(cls, nombre, coordenadas):
    nueva_zona = cls(nombre = nombre,coordenadas=coordenadas, estado=1, color="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
    db.session.add(nueva_zona)
    db.session.commit()
    return True
  

  @classmethod
  def obtener_coordenadas(cls, nombre):
    zona = cls.query.filter_by(nombre=nombre).first()
    if (zona):
      return zona.coordenadas
    else:
      return None
  

  @classmethod
  def actualizar_coordenadas(cls, name, coordenadas):
    zona = cls.query.filter_by(nombre=name).first()
    zona.coordenadas = coordenadas
    db.session.commit()
    return zona
  

  @classmethod
  def activar_zona(cls, id):
    zona = cls.query.filter_by(id=id).first()
    zona.estado = 1
    db.session.commit()
    return zona
  

  @classmethod
  def desactivar_zona(cls, id):
    zona = cls.query.filter_by(id=id).first()
    zona.estado = 0
    db.session.commit()
    return zona
  

  @classmethod
  def eliminar_zona(cls, id):
    zona_retornar = cls.query.filter_by(id=id).first()
    zona = cls.query.filter_by(id=id).first()
    db.session.delete(zona)
    db.session.commit()
    return zona_retornar
  

  @classmethod
  def editar_zona(cls, id, color):
    zona = cls.query.filter_by(id=id).first()
    zona.color = color
    db.session.commit()
    return True
  
  
  @classmethod
  def obtener_activos(cls):
    return cls.query.filter_by(estado=1)

     