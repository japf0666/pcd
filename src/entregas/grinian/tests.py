import pytest
from clases import NaveEstelar, Almacen, Repuesto, Comandante, Operario
from enums import EClaseNave
from sistema import Sistema
from excepciones import *



@pytest.fixture
def repuesto_base():
    return Repuesto("Motor", "Kuat", 10, 500.0)

@pytest.fixture
def sistema_preparado():
    sistema = Sistema()
    almacen = Almacen("Almacen Central", "Endor")
    nave = NaveEstelar("Ejecutor", "ID-1", 1, 1, 1, EClaseNave.EJECUTOR)
    
    cmd = Comandante("CMD-1", "Vader", nave)
    op = Operario("OP-1", "TK421", almacen)
    
    sistema.registrar_almacenes(almacen)
    sistema.registrar_naves(nave)
    sistema.registrar_usuario(cmd)
    sistema.registrar_usuario(op)
    
    repuesto = Repuesto("Deflector", "Sienar", 10, 100.0)
    almacen.agregar_repuesto(repuesto)
    
    return sistema, almacen, nave, cmd, op, repuesto


def test_crear_repuesto_valido(repuesto_base):
    assert repuesto_base.get_nombre() == "Motor"
    assert repuesto_base.get_cantidad() == 10

def test_repuesto_cantidad_negativa():
    with pytest.raises(ValueError):
        Repuesto("Motor", "Kuat", -5, 500.0)

def test_repuesto_coste_negativo():
    with pytest.raises(ValueError):
        Repuesto("Motor", "Kuat", 10, -100.0)

def test_repuesto_set_cantidad_negativa(repuesto_base):
    with pytest.raises(ValueError):
        repuesto_base.set_cantidad(-1)

def test_almacen_agregar_repuesto():
    a = Almacen("Base Hoth", "Hoth")
    r = Repuesto("Cable", "Sienar", 50, 10.0)
    a.agregar_repuesto(r)
    assert len(a.get_catalogo()) == 1

def test_almacen_buscar_repuesto_existe():
    a = Almacen("Base Hoth", "Hoth")
    r = Repuesto("Cable", "Sienar", 50, 10.0)
    a.agregar_repuesto(r)
    encontrado = a.buscar_repuesto("Cable")
    assert encontrado.get_nombre() == "Cable"

def test_almacen_buscar_repuesto_no_existe():
    a = Almacen("Base Hoth", "Hoth")
    encontrado = a.buscar_repuesto("Deflector")
    assert encontrado == -1

def test_nave_atributos():
    n = NaveEstelar("Ejecutor", "ID-1", 123, 1000, 500, EClaseNave.EJECUTOR)
    assert n.get_nombre() == "Ejecutor"
    assert len(n.get_repuestos()) == 0



def test_registrar_usuario(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    assert len(sistema.get_usuarios()) == 2

def test_iniciar_sesion_exito(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("CMD-1")
    assert sistema.get_usuario_activo() is not None
    assert sistema.get_usuario_activo().nombre == "Vader"

def test_iniciar_sesion_fallo(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("FALSO-ID")
    assert sistema.get_usuario_activo() is None

def test_cerrar_sesion(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("CMD-1")
    sistema.cerrar_sesion()
    assert sistema.get_usuario_activo() is None


def test_adquirir_repuesto_exito(sistema_preparado):
    sistema, _, nave, _, _, repuesto = sistema_preparado
    sistema.iniciar_sesion("CMD-1")
    sistema.adquirir_repuesto("Deflector", "Almacen Central", 2)
    
    assert repuesto.get_cantidad() == 8
    assert len(nave.get_repuestos()) == 1

def test_adquirir_repuesto_sin_stock(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("CMD-1")
    with pytest.raises(StockInsuficienteError):
        sistema.adquirir_repuesto("Deflector", "Almacen Central", 20)

def test_adquirir_repuesto_denegado(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("OP-1") 
    with pytest.raises(AccesoDenegadoError):
        sistema.adquirir_repuesto("Deflector", "Almacen Central", 2)

def test_adquirir_repuesto_almacen_falso(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("CMD-1")
    with pytest.raises(ValueError):
        sistema.adquirir_repuesto("Deflector", "Almacen Falso", 2)

def test_crear_repuesto_exito(sistema_preparado):
    sistema, almacen, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("OP-1")
    sistema.crear_repuesto("Motor", "Kuat", 5, 200.0)
    encontrado = almacen.buscar_repuesto("Motor")
    assert encontrado != -1

def test_crear_repuesto_duplicado(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("OP-1")
    with pytest.raises(ValueError):
        sistema.crear_repuesto("Deflector", "Sienar", 5, 200.0)

def test_actualizar_stock_exito(sistema_preparado):
    sistema, _, _, _, _, repuesto = sistema_preparado
    sistema.iniciar_sesion("OP-1")
    sistema.actualizar_stock("Deflector", 5)
    assert repuesto.get_cantidad() == 15

def test_actualizar_stock_no_existe(sistema_preparado):
    sistema, _, _, _, _, _ = sistema_preparado
    sistema.iniciar_sesion("OP-1")
    with pytest.raises(ValueError):
        sistema.actualizar_stock("PiezaFalsa", 5)