
from datetime import datetime
from random import choice, randint
from app.models.configuracion import Configuracion
from app.models.denuncia_categoria import DenunciaCategoria
from app.models.denuncia_estado import DenunciaEstado
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash as genph


def crear_administrador():
    lista_roles=[]
    fecha_actual = datetime.now()
    administrador = Usuario(usuario='admin', clave=genph('admin'), nombre='admin', apellido='admin', email='administrador@gmail.com', roles=lista_roles,activo=True,fecha_actualizacion=fecha_actual, fecha_creacion=fecha_actual)
    return administrador

def crear_operador():
    lista_roles=[]
    fecha_actual = datetime.now()
    operador = Usuario(usuario='operador', clave=genph('operador'), nombre='operador', apellido='operador', email='operador@gmail.com', roles=lista_roles ,activo=True, fecha_actualizacion=fecha_actual, fecha_creacion=fecha_actual)
    return operador

def asignar_permisos(db, administrador, operador):
    # Permisos
    # Permisos punto de encuentro
    punto_encuentro_index = Permiso("punto_encuentro_index")       # 1.permite acceder al index (listado) del módulo.
    punto_encuentro_new = Permiso("punto_encuentro_new")           # 2.permite cargar una zona inundable.
    punto_encuentro_destroy = Permiso("punto_encuentro_destroy")   # 3.permite borrar una zona inundable.
    punto_encuentro_update = Permiso("punto_encuentro_update")     # 4.permite actualizar una zona inundable.
    punto_encuentro_show = Permiso("punto_encuentro_show")         # 5.permite visualizar una zona inundable.
    # Permisos usuario
    usuario_index = Permiso("usuario_index")                       # 6.permite acceder a los módulos del usuario.
    usuario_new = Permiso("usuario_new")                           # 7.permite cargar un usuario.
    usuario_destroy = Permiso("usuario_destroy")                   # 8.permite borrar un usuario.
    usuario_update = Permiso("usuario_update")                     # 9.permite actualizar un usuario.
    usuario_show = Permiso("configuracion_show")                   # 10.permite visualizar una usuario.
    # Permisos configuracion
    configuracion_index = Permiso("configuracion_index")           # 11.permite acceder a las configuraciones 
    configuracion_new = Permiso("configuracion_new")               # 12.permite cargar configuraciones.
    configuracion_destroy = Permiso("configuracion_destroy")       # 13.permite borrar una configuracion.
    configuracion_update = Permiso("configuracion_update")         # 14.permite actualizar la configuracion.
    configuracion_show = Permiso("configuracion_show")             # 15.permite visualizar la configuracion.
    # Permisos denuncia
    denuncia_index = Permiso("denuncia_index")                     # 16.permite acceder a las denuncias
    denuncia_create = Permiso("denuncia_create")                   # 17.permite cargar denuncias.
    denuncia_destroy = Permiso("denuncia_destroy")                 # 18.permite borrar una denuncia.
    denuncia_update = Permiso("denuncia_update")                   # 19.permite actualizar una denuncia.
    denuncia_show = Permiso("denuncia_show")                       # 20.permite visualizar las denuncias.
    # Permisos zonas
    zonas_index = Permiso("zonas_index")                           # 21.permite acceder a las zonas
    zonas_import = Permiso("zonas_import")                         # 22.permite importar archivos csv
    zonas_destroy = Permiso("zonas_destroy")                       # 23.permite borrar una zona.
    zonas_show = Permiso("zonas_show")                             # 24.permite visualizar las zonas.
    # Permisos recorrido
    recorrido_index = Permiso("recorrido_index")                   # 25.permite acceder a los recorridos
    recorrido_create = Permiso("recorrido_create")                 # 26.permite cargar recorridos
    recorrido_destroy = Permiso("recorrido_destroy")               # 27.permite borrar recorridos.
    recorrido_update = Permiso("recorrido_update")                 # 28.permite actualizar recorridos
    recorrido_show = Permiso("recorrido_show")                     # 29.permite visualizar recorridos
    # Permisos google
    usuario_google = Permiso("usuario_google")                     # 30.permite aceptar/rechazar usuarios de google
    # Roles
    rol_admin = Rol("Administrador")
    rol_operador = Rol("Operador")
    # Asignar
    # Asignar al administrador todos los permisos
    rol_admin.asignar_permiso(punto_encuentro_index)
    rol_admin.asignar_permiso(punto_encuentro_new)
    rol_admin.asignar_permiso(punto_encuentro_destroy)
    rol_admin.asignar_permiso(punto_encuentro_update)
    rol_admin.asignar_permiso(punto_encuentro_show)
    rol_admin.asignar_permiso(usuario_index)
    rol_admin.asignar_permiso(usuario_new)
    rol_admin.asignar_permiso(usuario_destroy)
    rol_admin.asignar_permiso(usuario_update)
    rol_admin.asignar_permiso(usuario_show)
    rol_admin.asignar_permiso(configuracion_index)
    rol_admin.asignar_permiso(configuracion_new)
    rol_admin.asignar_permiso(configuracion_destroy)
    rol_admin.asignar_permiso(configuracion_update)
    rol_admin.asignar_permiso(configuracion_show)
    rol_admin.asignar_permiso(denuncia_index)
    rol_admin.asignar_permiso(denuncia_create)
    rol_admin.asignar_permiso(denuncia_destroy)
    rol_admin.asignar_permiso(denuncia_update)
    rol_admin.asignar_permiso(denuncia_show)
    rol_admin.asignar_permiso(zonas_index)
    rol_admin.asignar_permiso(zonas_import)
    rol_admin.asignar_permiso(zonas_destroy)
    rol_admin.asignar_permiso(zonas_show)
    rol_admin.asignar_permiso(recorrido_index)
    rol_admin.asignar_permiso(recorrido_create)
    rol_admin.asignar_permiso(recorrido_destroy)
    rol_admin.asignar_permiso(recorrido_update)
    rol_admin.asignar_permiso(recorrido_show)
    rol_admin.asignar_permiso(usuario_google)
    # Asignar al operador algunos permisos
    rol_operador.asignar_permiso(usuario_update)
    rol_operador.asignar_permiso(denuncia_index)
    rol_operador.asignar_permiso(denuncia_create)
    rol_operador.asignar_permiso(denuncia_update)
    rol_operador.asignar_permiso(denuncia_show)
    rol_operador.asignar_permiso(zonas_index)
    rol_operador.asignar_permiso(zonas_import)
    rol_operador.asignar_permiso(zonas_show)
    rol_operador.asignar_permiso(recorrido_index)
    rol_operador.asignar_permiso(recorrido_create)
    rol_operador.asignar_permiso(recorrido_update)
    rol_operador.asignar_permiso(recorrido_show)
    

    administrador.roles.append(rol_admin)
    operador.roles.append(rol_operador)

    db.session.add_all(
        [
            rol_admin,
            rol_operador,
            administrador,
            operador,
            punto_encuentro_index,
            punto_encuentro_new,
            punto_encuentro_destroy,
            punto_encuentro_update,
            punto_encuentro_show,
            usuario_index,
            usuario_new,
            usuario_destroy,
            usuario_update,
            usuario_show,
            configuracion_index,
            configuracion_new,
            configuracion_destroy,
            configuracion_update,
            configuracion_show,
            denuncia_index,
            denuncia_create,
            denuncia_destroy,
            denuncia_update,
            denuncia_show,
            zonas_index,
            zonas_import,
            zonas_destroy,
            zonas_show,
            recorrido_index,
            recorrido_create,
            recorrido_destroy,
            recorrido_update,
            recorrido_show,
            usuario_google,
        ]
    )
    return db

def crear_configuracion(db):
    lista_aleatoria=['red','blue','yellow']
    configuracion = Configuracion(randint(5,10),'descendente',choice(lista_aleatoria),choice(lista_aleatoria),choice(lista_aleatoria))
    db.session.add(configuracion)
    return db

def crear_estados_categoria_denuncia(db):
     # Creo estados, categorias y seguimiento
    # Le asignamos los id para los listados
    denuncia_estado_sin_confirmar = DenunciaEstado(1,"Sin confirmar")
    denuncia_estado_en_curso = DenunciaEstado(2,"En curso")
    denuncia_estado_resuelta = DenunciaEstado(3,"Resuelta")
    denuncia_estado_cerrada = DenunciaEstado(4,"Cerrada")
    denuncia_categoria_alcantarrila_tapada = DenunciaCategoria("Alcantarilla tapada")
    denuncia_categoria_basural = DenunciaCategoria("Basural")
    denuncia_categoria_desperfecto_natural = DenunciaCategoria("Desperfecto natural")
    
    db.session.add_all(
        [
            denuncia_estado_sin_confirmar,
            denuncia_estado_en_curso,
            denuncia_estado_resuelta,
            denuncia_estado_cerrada,
            denuncia_categoria_alcantarrila_tapada,
            denuncia_categoria_basural,
            denuncia_categoria_desperfecto_natural,
        ]
    )
    return db




# Se debe entregar el sistema con el administrador y la configuracion cargada.
def cargar(db):
    administrador = crear_administrador()
    operador = crear_operador()
    asignar_permisos(db, administrador, operador)
    db = crear_configuracion(db)
    db = crear_estados_categoria_denuncia(db)
    db.session.commit() # escribir los cambios en la base de datos.