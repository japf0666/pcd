import pytest
from flota_imperial import (
    Ubicacion, ClaseNave,
    StockInsuficienteError, RepuestoNoEncontradoError,
    EstacionEspacial, NaveEstelar, CazaEstelar,
    Nave, UnidadCombate,
    Repuesto, Almacen
)

# FIXTURE

@pytest.fixture
def repuesto_basico():
    return Repuesto("Motor ion", "Sienar Fleet", 50, 1200.0)

@pytest.fixture
def almacen_con_stock():
    a = Almacen("Almacén Alpha", "Endor")
    a.agregar_repuesto(Repuesto("Motor ion", "Sienar Fleet", 50, 1200.0))
    a.agregar_repuesto(Repuesto("Panel solar", "Kuat Drive", 3, 450.0))
    return a

#  TESTS 

def test_estacion_espacial():
    e = EstacionEspacial("Estrella", [], 100, 50, Ubicacion.ENDOR)
    assert e._nombre == "Estrella"
    assert e._ubicacion == Ubicacion.ENDOR

def test_nave_estelar():
    n = NaveEstelar("Devastador", [], 100, 50, ClaseNave.EJECUTOR)
    assert n._clase == ClaseNave.EJECUTOR

def test_caza_es_nave_y_unidad_combate():
    c = CazaEstelar("TIE", [], 1, "ID-001", 12345)
    assert isinstance(c, Nave)
    assert isinstance(c, UnidadCombate)

def test_repuesto_cantidad_privada(repuesto_basico):
    assert repuesto_basico.get_cantidad() == 50

def test_consumir_stock_correcto(repuesto_basico):
    repuesto_basico.consumir_stock(10)
    assert repuesto_basico.get_cantidad() == 40

def test_stock_insuficiente(repuesto_basico):
    with pytest.raises(StockInsuficienteError):
        repuesto_basico.consumir_stock(999)

def test_repuesto_no_encontrado(almacen_con_stock):
    with pytest.raises(RepuestoNoEncontradoError):
        almacen_con_stock.buscar_repuesto("Sable de luz")

def test_buscar_repuesto_existente(almacen_con_stock):
    r = almacen_con_stock.buscar_repuesto("Motor ion")
    assert r.nombre == "Motor ion"