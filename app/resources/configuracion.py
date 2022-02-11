from flask import render_template, request
from app.models.configuracion import Configuracion
from app.helpers import permisos
from app.validaciones.validar_configuracion import ValidarConfiguracion


def vista_configuracion():
    permisos.validar_permisos('configuracion_index')
    actual = Configuracion.todo()
    if request.method == 'POST':
        datos = request.form
        errores = ValidarConfiguracion(datos).validar()
        if not errores:
            Configuracion.editar(datos["cantPagina"], datos['criterio'], datos["color_p"], datos["color_s"], datos["color_t"] )
            mensaje = "Se modifico la tabla configuracion correctamente"  
            configuracion = Configuracion.obtener_configuracion() 
            return render_template('/index.html', mensaje=mensaje, configuracion=configuracion)
        else:
            return render_template("configuracion/configuracion.html", errores=errores)

    elif request.method == 'GET':
        return render_template("configuracion/configuracion.html", actual=actual)
