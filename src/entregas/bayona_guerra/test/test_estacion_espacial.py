import pytest 
from Imperio_Galactico import EstacionEspacial, EUbicacion

# --- TEST ---

def test_estacion_calculo_capacidad():
    """Verifica que la capacidad total sea la suma de tripulación y pasaje."""
    estacion = EstacionEspacial("1234", 1234, "Estacion1", [], 10, 50, EUbicacion.ENDOR)
    assert estacion.calcularCapacidad() == 60

def test_estacion_error_tripulacion_no_int():
    """Verifica TypeError si la tripulación no es un entero."""
    with pytest.raises(TypeError, match="tripulacion debe ser un numero entero"):
        EstacionEspacial("1234", 1234, "Estacion1", [], "10", 50, EUbicacion.ENDOR)

def test_estacion_error_pasaje_no_int():
    """Verifica TypeError si el pasaje no es un entero."""
    with pytest.raises(TypeError, match="pasaje debe ser un numero entero"):
        EstacionEspacial("1234", 1234, "Estacion1", [], 10, 50.5, EUbicacion.ENDOR)

def test_estacion_error_ubicacion_invalida():
    """Verifica TypeError si la ubicación no es del tipo EUbicacion."""
    with pytest.raises(TypeError, match="ubicacion debe estar contenido en la enumeracion"):
        EstacionEspacial("1234", 1234, "Estacion1", [], 10, 50, "MARTE")

def test_estacion_error_valores_negativos():
    """Verifica ValueError si se introducen números negativos."""
    with pytest.raises(ValueError, match="debe ser positivo"):
        EstacionEspacial("1234", 1234, "Estacion1", [], -5, 50, EUbicacion.ENDOR)

def test_estacion_actualizar_ubicacion_correcta():
    """Verifica que la ubicación se actualiza correctamente con un Enum válido."""
    estacion = EstacionEspacial("1234", 1234, "Estacion1", [], 10, 50, EUbicacion.ENDOR)
    estacion.actualizarUbicacion(EUbicacion.CUMULO_RAIMOS)

def test_estacion_actualizar_ubicacion_error():
    """Verifica que actualizarUbicacion lanza TypeError con datos inválidos."""
    estacion = EstacionEspacial("1234", 1234, "Estacion1", [], 10, 50, EUbicacion.ENDOR)
    with pytest.raises(TypeError, match="nueva_ubicacion debe estar en la lista de ubicaciones disponibles"):
        estacion.actualizarUbicacion(2)