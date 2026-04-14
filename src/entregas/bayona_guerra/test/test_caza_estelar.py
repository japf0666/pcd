import pytest
from Imperio_Galactico import CazaEstelar, AccesoDenegado

# --- TESTS ---

def test_caza_creacion_correcta():
    """Verifica que un CazaEstelar se cree con los atributos adecuados."""
    catalogo = ["Cañon", "Motor"]
    caza = CazaEstelar("12345", 6789, "Estrella de la muerte", catalogo, 1)
    
    # Verificamos herencia y atributos
    assert "Cañon" in caza.consultarCatalogo()
    # Como dotación es privado, no lo testeamos directamente, 
    # pero verificamos que no falló la creación.

def test_caza_error_dotacion_no_int():
    """Verifica TypeError si la dotación no es un entero."""
    with pytest.raises(TypeError, match="dotacion TIENE QUE SER int"):
        CazaEstelar("12345", 6789, "Estrella de la muerte", [], "uno")

def test_caza_error_dotacion_negativa():
    """Verifica ValueError si la dotación es menor que 0."""
    with pytest.raises(ValueError, match="dotacion debe ser positivo o 0"):
        CazaEstelar("12345", 6789, "Estrella de la muerte", [], -1)

def test_caza_desplegar_piloto_con_dotacion(capsys):
    """Verifica que se imprima el mensaje de despliegue si hay dotación."""
    caza = CazaEstelar("24680", 1111, "Halcon Milenario", [], 2)
    caza.desplegarPiloto()
    
    captured = capsys.readouterr()
    assert "Piloto desplegado" in captured.out
    assert "Quedan 1 pilotos por desplegar" in captured.out

def test_caza_desplegar_piloto_sin_dotacion(capsys):
    """Verifica el mensaje de error si la dotación es 0."""
    caza = CazaEstelar("12345", 0000, "Caza1", [], 0)
    caza.desplegarPiloto()
    
    captured = capsys.readouterr()
    assert "No se puede desplegar ningun piloto" in captured.out

def test_caza_transmision_mensaje_correcta(capsys):
    """Verifica la transmisión con clave correcta."""
    clave = 9999
    caza = CazaEstelar("13579", clave, "Caza2", [], 1)
    
    caza.transmitirMensaje("Objetivo a la vista", clave)
    
    captured = capsys.readouterr()
    assert "Caza Estelar 13579: Objetivo a la vista" in captured.out

def test_caza_transmision_mensaje_error_clave():
    """Verifica que falla con clave incorrecta lanzando AccesoDenegado."""
    caza = CazaEstelar("13579", 9999, "Caza2", [], 1)
    
    with pytest.raises(AccesoDenegado):
        caza.transmitirMensaje("Mensaje secreto", 0000)