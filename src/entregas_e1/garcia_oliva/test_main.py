import pytest
from entregable1 import Repuesto, Almacen, Comandante, CantidadInvalidaError, RepuestoNoEncontrado


def test_repuesto_cantidad_negativa():
    # hacemos este test para comprobar que la excepción personalizada funciona bien
    with pytest.raises(CantidadInvalidaError):
        Repuesto("Motor", "TSLA", -5, 100.0)


def test_creacion_repuesto_valido():
    # este test comprueba que la inizalización de Repuesto se ejecuta correctamente
    repu = Repuesto("Motor", "TSLA", 10, 100.0)
    assert repu.getCantidad(
    ) == 10 and repu.nombre == "Motor" and repu.precio == 100.0 and repu.proveedor == "TSLA"


def test_almacen_add_buscar():
    # este test comprueba que la búsqueda de repuestos en almacenes funciona
    almacen = Almacen("GigaTexas", "Texas")
    repu = Repuesto("Motor", "TSLA", 10, 100.0)
    almacen.addCatalogo(repu)
    assert almacen.buscarRepuesto("Motor") == repu


def test_excepcion_repuesto_no_encontrado():
    # comprubea la otra excepción personalizada
    almacen = Almacen("GigaTexas", "Texas")
    with pytest.raises(RepuestoNoEncontrado):
        almacen.buscarRepuesto("Motor")


def test_comandante_adquirir_repuesto():
    # comprueba que la función de adquirir actualiza correctamente la cantidad
    almacen = Almacen("GigaTexas", "Texas")
    repu = Repuesto("Motor", "TSLA", 10, 100.0)
    almacen.addCatalogo(repu)
    coman = Comandante("Elon Musk", "CMD-420")
    coman.adquirirRepuesto(almacen, "Motor", 3)
    assert almacen.buscarRepuesto("Motor").getCantidad() == 7
