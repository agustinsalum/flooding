from flask import session, abort
from app.helpers.auth import authenticated

def validar_permisos(un_permiso):

	if not authenticated(session):
		print("Salio xq no estaba autenticado")
		abort(401)
	if not usuario_activo(session):
		print("Salio xq no estaba activo")
		abort(403)
	if un_permiso != '' and not tiene_el_permiso(un_permiso):
		print("Se solicito permiso para "+ un_permiso)
		print("Salio xq no tenia el permiso")
		abort(403)
	return

def tiene_el_permiso(un_permiso):
	return session["usuario"].tiene_permiso(un_permiso)

def usuario_activo(session):
	try:
		return session["usuario"].activo
	except (AttributeError):
		# Para los usuarios de google
		return session["usuario"].aprobado
