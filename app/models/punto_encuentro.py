from app.db import db


#clase punto de encuentro
class PuntoEncuentro(db.Model):
   __tablename__= 'punto_encuentro'
   id_punto = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(40))
   direccion = db.Column(db.String(60))
   latitud = db.Column(db.Text)
   longitud = db.Column(db.Text)
   estado = db.Column(db.Integer)
   telefono = db.Column(db.String(20))
   email = db.Column(db.String(60))
   

   @classmethod
   def filtrar_por_nombre(cls,nombre):
      return cls.query.filter(cls.nombre.contains(nombre))


   @classmethod
   def todo(cls):
      return cls.query.all()   

   
   @classmethod
   def crear(cls,nombre , direccion, latitud, longitud, estado, telefono, email):
      nuevo_punto = cls (nombre = nombre, direccion = direccion, latitud = latitud, longitud = longitud, estado = estado, telefono = telefono, email = email)
      db.session.add(nuevo_punto)
      db.session.commit()
      return True
   
   
   @classmethod
   def obtener_por_id(cls,id):
      # Dado el id obtenemos la instancia
      return cls.query.get(id)

   
   @classmethod
   def editar(cls, id, nombre, direccion, telefono, email, latitud, longitud):
      datos = cls.query.filter_by(id_punto=id).first()
      datos.nombre = nombre
      datos.direccion = direccion
      datos.telefono = telefono
      datos.email = email
      datos.latitud = latitud
      datos.longitud = longitud
      db.session.commit()
      return datos

   
   @classmethod
   def publicar_punto(cls,id_punto):
      datos = cls.query.filter_by(id_punto=id_punto).first()
      print ("entre_publicar")
      print (datos.estado)
      datos.estado = 1
      db.session.commit()
      return datos

   
   @classmethod
   def despublicar_punto(cls, id):
      datos = cls.query.filter_by(id_punto=id).first()
      print ("entre_despublicar")
      print (datos.estado)
      datos.estado = 0
      db.session.commit()
      return datos

   
   @classmethod
   def borrar_punto(cls,id):
      datos = cls.query.filter_by(id_punto=id).first()
      datos.id_punto = id
      db.session.delete(datos)
      db.session.commit()
      return True
      
   
   @classmethod
   def obtener_activos(cls):
        return cls.query.filter_by(estado=1)

