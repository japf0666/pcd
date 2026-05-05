import pytest
from Imperio_Galactico import NaveEstelar, EClaseNave

# --- TESTS ---

def test_nave_estelar_creacion_correcta():
    """Verifica que los atributos se asignen correctamente, incluyendo el Enum."""
    nave = NaveEstelar("1234", 9999, "Nave1", ["Motor", "Escudo"], 5000, 100, EClaseNave.EJECUTOR)
    
    assert nave.obtenerClase() == EClaseNave.EJECUTOR
    assert "Motor" in nave.consultarCatalogo()

def test_nave_estelar_error_tripulacion_str():
    """Verifica TypeError si la tripulación es un string."""
    with pytest.raises(TypeError, match="tripulacion debe ser un numero entero"):
        NaveEstelar("1234", 1, "Nave2", [], "cinco", 0, EClaseNave.EJECUTOR)

def test_nave_estelar_error_clase_invalida():
    """Verifica que la clase debe ser obligatoriamente un miembro de EClaseNave."""
    match_error = "clase tiene que pertenecer a la enumeracion referente a las clases de las naves estelares"
    with pytest.raises(TypeError, match=match_error):
        NaveEstelar("1234", 1, "Nave2", [], 100, 0, "EJECUTOR")

def test_nave_estelar_obtener_clase():
    """Verifica que el método getter devuelva el objeto Enum esperado."""
    clase_esperada = EClaseNave.ECLIPSE
    nave = NaveEstelar("5678", 123, "Nave3", [], 10000, 500, clase_esperada)
    
    assert nave.obtenerClase() == clase_esperada
    assert isinstance(nave.obtenerClase(), EClaseNave)

def test_nave_estelar_transmision_mensaje(capsys):
    """Verifica que el mensaje se imprima con el formato correcto."""
    clave_test = 000
    nave = NaveEstelar("1357", clave_test, "Nave4", [], 10, 0, EClaseNave.SOBERANO)
    
    nave.transmitirMensaje("Alerta de rebeldes", clave_test)
    
    captured = capsys.readouterr()
    assert "Nave Estelar 1357: Alerta de rebeldes" in captured.out