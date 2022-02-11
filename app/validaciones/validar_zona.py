
from app.models.zona import Zona


class ValidarZona(Zona):

    def no_existe_archivo(archivo):
        if not archivo:
            return True
        return False
    
    
    def no_existe_cabecera(array):
        return (len(array[0]) == 0)

