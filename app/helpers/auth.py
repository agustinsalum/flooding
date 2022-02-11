def authenticated(session):
    user = session.get("usuario")
    if user:
        return True
    else:
        return False

def usuario(session):
    user = session.get("usuario")
    return user.usuario