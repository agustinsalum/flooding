from app.models.configuracion import Configuracion


def obtener_configuracion():
      return Configuracion.obtener_configuracion()


def obtener_configuracion_color_primario():
 configuracion = Configuracion.obtener_configuracion().color_primario
 return {
       'red': 'priRojo',
       'blue': 'priAzul',
       'yellow': 'priAma'
       }.get(configuracion, 'priAzul')


def obtener_configuracion_color_secundario():
 configuracion = Configuracion.obtener_configuracion().color_secundario
 return {
       'red': 'secRojo',
       'blue': 'secAzul',
       'yellow': 'secAma'
       }.get(configuracion, 'secAzul')


def obtener_configuracion_color_terciario():
 configuracion = Configuracion.obtener_configuracion().color_terciario
 return {
       'red': 'terRojo',
       'blue': 'terAzul',
       'yellow': 'terAma'
       }.get(configuracion, 'terAzul')


def configurated(session):
   return session.get('config')
    