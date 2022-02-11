from app.db import db

class Recorrido(db.Model):
  __tablename__ = 'recorrido_evacuacion'
  id_recorrido = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(40))
  descripcion = db.Column(db.Text)
  estado = db.Column(db.String(40))
  coordenadas = db.Column(db.String(255))

  
  @classmethod
  def todo(cls):
    return cls.query.all()

  
  @classmethod
  def obtener_por_id(cls, recorrido_id):
    # Dado el id obtenemos la instancia
    return cls.query.get(recorrido_id)
  

  @classmethod
  def filtrar_por_nombre(cls,name):
    return cls.query.filter(Recorrido.nombre.contains(name))



  @classmethod
  def crear(cls, nombre, descripcion, estado, arreglo_coordenadas):
    nuevo_usuario = cls(nombre = nombre, descripcion = descripcion, estado = estado, coordenadas = arreglo_coordenadas)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return True

  
  @classmethod
  def borrar_recorrido(cls,recorrido_id):
    datos = cls.query.filter_by(id_recorrido=recorrido_id).first()
    datos.id_recorrido = recorrido_id
    db.session.delete(datos)
    db.session.commit()
    return True

  
  @classmethod
  def publicar_recorrido(cls, idR):
    datos = cls.query.filter_by(id_recorrido = idR).first()
    datos.estado = 1
    db.session.commit()
    return datos

  
  @classmethod
  def despublicar_recorrido(cls, recorrido_id):
    datos = cls.query.filter_by(id_recorrido = recorrido_id).first()
    datos.estado = 0
    db.session.commit()
    return datos

  
  @classmethod
  def editar(cls, id, nombre, coordenadas, descripcion):
    datos = cls.query.filter_by(id_recorrido=id).first()
    datos.nombre = nombre
    datos.coordenadas = coordenadas
    datos.descripcion = descripcion
    db.session.commit()
    return datos
  
  
  @classmethod
  def obtener_activos(cls):
    return cls.query.filter_by(estado=1)