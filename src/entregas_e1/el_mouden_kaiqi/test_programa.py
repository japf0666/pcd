import pytest
from entregable2_0 import Ubicacion, ClaseNave, EstacionEspacial, NaveEstelar, CazaEstelar, Repuesto, Almacen



#==================== TESTS PARA REPUESTOS ====================



def test_crear_repuesto():
    repuesto = Repuesto("motor", 10, 5000.0)
    assert repuesto.get_nombre() == "motor"
    assert repuesto.get_cantidad() == 10
    assert repuesto.get_precio() == 5000.0

def test_añadir_stock():
    repuesto = Repuesto("escudo", 5, 8000.0)
    repuesto.añadir_stock(3)
    assert repuesto.get_cantidad() == 8

def test_retirar_stock():
    repuesto = Repuesto("laser", 5, 1000.0)
    repuesto.retirar_stock(2)
    assert repuesto.get_cantidad() == 3

def test_set_cantidad_negativa():
    repuesto = Repuesto("ala", 10, 500.0)
    with pytest.raises(ValueError):
        repuesto.set_cantidad(-5)



# ==================== TESTS PARA ALMACENES ====================
 


def test_crear_almacen():
    almacen = Almacen("Alfa", "Hangar")
    assert almacen.get_nombre() == "Alfa"

def test_añadir_repuesto():
    almacen = Almacen("Beta", "Sector 7")
    repuesto = Repuesto("motor", 5, 1000.0)
    almacen.añadir_repuesto(repuesto)
    assert almacen.consultar_stock("motor") == 5

def test_eliminar_repuesto():
    almacen = Almacen("Gamma", "Base")
    repuesto = Repuesto("escudo", 3, 2000.0)
    almacen.añadir_repuesto(repuesto)
    almacen.eliminar_repuesto("escudo")
    assert almacen.consultar_stock("escudo") == 0

def test_actualizar_stock_insuficiente():
    almacen = Almacen("Delta", "Orbita")
    repuesto = Repuesto("panel", 2, 100.0)
    almacen.añadir_repuesto(repuesto)
    with pytest.raises(Exception):
        almacen.actualizar_stock("panel", 5)

# ==================== TESTS PARA NAVES ====================

def test_estacion_espacial():
    estacion = EstacionEspacial(
       "Estación Endor", ["Generador"], "ES-001", 9999,
       5000, 1000, Ubicacion.ENDOR
        )
    assert estacion.get_ubicacion() == "Endor"

def test_nave_estelar():
    nave = NaveEstelar(
        "Executor", ["Motor"], "DS-001", 7734,
        280000, 5000, ClaseNave.EJECUTOR
    )
    assert nave.get_clase() == "Ejecutor"

def test_caza_estelar():
    caza = CazaEstelar(
        "TIE Fighter", ["Panel"], "TF-042", 1138, 1
    )
    assert caza.get_dotacion() == 1

def test_añadir_repuesto_nave():
    nave = NaveEstelar(
       "Nave Test", [], "NT-001", 1111,
        10, 5, ClaseNave.SOBERANO
    )
    nave.añadir_repuesto("motor")
    assert "motor" in nave.consultar_repuesto()


# ==================== TESTS PARA ENUMERACIONES ====================

def test_ubicacion_enum():
    assert Ubicacion.ENDOR.value == "Endor"
    assert Ubicacion.CUMULO_RAIMOS.value == "Cúmulo Raimos"

def test_clase_nave_enum():
    assert ClaseNave.EJECUTOR.value == "Ejecutor"
    assert ClaseNave.ECLIPSE.value == "Eclipse"
