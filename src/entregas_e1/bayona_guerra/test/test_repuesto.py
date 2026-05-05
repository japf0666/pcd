import pytest
from Imperio_Galactico import Repuesto

# --- TESTS ---

def test_creacion_repuesto():
    """Verifica que los atributos se asignen correctamente al iniciar."""
    r = Repuesto("Tornillo", "Mercadona", 50, 1200.50)
    assert r.nombre == "Tornillo"
    assert r.obtenerUnidades() == 50
    assert r.precio == 1200.50

def test_gestion_stock():
    """Prueba el ciclo de vida del stock: aumentar y reducir."""
    r = Repuesto("Tuerca", "Carrefour", 10, 100.0)
    
    # Aumentar
    r.aumentarStock(5)
    assert r.obtenerUnidades() == 15
    
    # Reducir
    r.reducirStock(8)
    assert r.obtenerUnidades() == 7

def test_error_stock_insuficiente():
    """Verifica que no se pueda reducir más de lo que hay."""
    r = Repuesto("Rueda", "Spar", 5, 500.0)
    with pytest.raises(ValueError):
        r.reducirStock(10)

def test_error_tipo_precio():
    """Verifica que el precio no acepte strings (debe ser int o float)."""
    with pytest.raises(TypeError):
        Repuesto("Ala", "Lidl", 10, "Gratis")

def test_error_cantidad_no_entera():
    """Verifica que la cantidad en aumentarStock sea obligatoriamente int."""
    r = Repuesto("Ala", "Lidl", 10, 5.0)
    with pytest.raises(TypeError):
        r.aumentarStock(5.5)