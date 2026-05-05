import pytest
from Imperio_Galactico import UnidadCombate, AccesoDenegado

''' Como UnidadCombate es una clase abstracta, no podemos crearla directamente.
    Creamos una clase hija mínima solo para poder testear la lógica del padre.'''

class UnidadCombatePrueba(UnidadCombate):
    def transmitirMensaje(self, mensaje: str) -> None:
        pass 

def test_creacion_unidad_correcta():
    """Verifica que una unidad se crea con datos válidos."""
    unidad = UnidadCombatePrueba("1234", 1234)
    assert unidad._idCombate == "1234"
    assert unidad._claveCifrada == 1234

def test_error_tipo_id_combate():
    """Verifica que lanza TypeError si el ID no es un string."""
    with pytest.raises(TypeError):
        UnidadCombatePrueba(1234, 1234) # Enviamos un int en lugar de str

def test_autenticacion_exitosa():
    """Verifica que devuelve True si la clave coincide."""
    unidad = UnidadCombatePrueba("5678", 9999)
    assert unidad.autentificarClave(9999) is True

def test_excepcion_acceso_denegado():
    """Verifica que lanza nuestra excepción personalizada si la clave falla."""
    unidad = UnidadCombatePrueba("5678", 9999)
    
    # Solo comprobamos que la excepción ocurre al meter la clave mal
    with pytest.raises(AccesoDenegado):
        unidad.autentificarClave(1111)