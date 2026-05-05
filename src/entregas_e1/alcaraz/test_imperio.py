import pytest
from MiImperio import Repuesto, Almacen, SinStockError, CazaEstelar, Comandante


# ==========================================
# --- TESTS UNITARIOS (Pytest) ---
# DECISIÓN DE DISEÑO: Utilizo pytest.raises para verificar que las
# excepciones personalizadas y las validaciones de Python saltan correctamente.
# ==========================================


# Test 1: Comprobar que salta el error de Stock
def test_sin_stock_error():
    repuesto = Repuesto("Tornillo", "Sienar", 1, 10.0)
    repuesto.retirar_stock() # Quedan 0
    with pytest.raises(SinStockError):
        repuesto.retirar_stock() # Debería fallar aquí

# Test 2: Comprobar que no se permiten precios negativos (ValueError)
def test_precio_negativo():
    with pytest.raises(ValueError):
        Repuesto("Ala-X", "Incom", 1, -500.0)

# Test 3: Comprobar que el almacén solo acepta objetos tipo Repuesto (TypeError)
def test_almacen_type_error():
    alm = Almacen("Test", "Endor")
    with pytest.raises(TypeError):
        alm.agregar_repuesto("Esto no es un repuesto, es un texto")

# Test 4: Comprobar que el Comandante maneja bien un objeto que no es una nave
def test_comandante_attribute_error(capsys):
    """Comprueba que el Comandante captura errores si el objetivo no es una Nave."""
    vader = Comandante("Vader")
    # Pasamos un número (12345) en lugar de un objeto Nave
    vader.comprar_repuesto(12345, None, "Cualquier cosa")
    
    # capsys captura lo que sale por la terminal (stdout)
    captured = capsys.readouterr()
    # Verificamos que nuestro mensaje de error controlado aparece en pantalla
    assert "ERROR CRÍTICO" in captured.out