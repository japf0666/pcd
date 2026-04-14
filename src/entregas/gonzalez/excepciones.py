# Excepcion personalizada para cuando el usuario no tiene permisos
class PermisoDenegadoError(Exception):
    pass
# Excepcion personalizada para errores relacionados con cantidades
class CantidadError(Exception):
    pass