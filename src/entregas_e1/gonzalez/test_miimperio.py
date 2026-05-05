import pytest
from enumeraciones import ClaseNaveEstelar, UbicacionEstacion
from naves import CazaEstelar, EstacionEspacial, NaveEstelar
from almacen_piezas import Almacen, Repuesto, OperarioAlmacen, Comandante
from miImperio import MiImperio
from excepciones import PermisoDenegadoError, CantidadError


def test_naves_clave_unica():
    n1 = NaveEstelar("NE1", ["Motor"], 10, 2, ClaseNaveEstelar.ECLIPSE)
    
    with pytest.raises(ValueError):
        n2 = EstacionEspacial("EE1", ["Repuesto"], 100, 12, "Murcia")

    n3 = CazaEstelar("C1", ["Ala"], 1)

    assert n3.clave != n1.clave, "La claves deben ser únicas"


def test_naves_metodos_basicos():
    n1 = NaveEstelar("NE1", ["Motor", "Ala"], 10, 2, ClaseNaveEstelar.ECLIPSE)
    

    assert n1.repuesto_valido("Motor") is True
    assert n1.repuesto_valido("X") is False
    
    assert "Motor" in n1.consultar_piezas()


def test_anadir_y_listar_naves_almacenes():
    imperio = MiImperio()
    n1 = NaveEstelar("NE1", ["Motor"], 10, 2, ClaseNaveEstelar.EJECUTOR)
    a1 = Almacen("Almacen1", "Tatooine")

    imperio.añadir_nave(n1)
    imperio.añadir_almacen(a1)

    assert list(imperio.mostrar_naves()) == [n1]
    assert list(imperio.mostrar_almacenes()) == [a1]

    # probar que no se pueden añadir objetos no válidos
    with pytest.raises(ValueError):
        imperio.añadir_nave("no es nave") 
    with pytest.raises(ValueError):
        imperio.añadir_almacen("no es almacen")


def test_almacen_operario_comandante():
    almacen = Almacen("Almacen1", "Tatooine")
    operario = OperarioAlmacen("Op1")
    nave = CazaEstelar("C1", ["Motor"], 4)
    comandante = Comandante("Com1", nave)

    almacen.añadir_operario(operario)
    almacen.añadir_comandante(comandante)

    # probar que no se pueda añadir alguien que no es un comandante
    with pytest.raises(ValueError):
        almacen.añadir_comandante("Pedro")

    rep = Repuesto("Motor", "ProveedorA", 10, 1500.0)
    operario.añadir_repuesto(rep, almacen)

    assert "Motor" in almacen.catalogo_piezas
    assert almacen.catalogo_piezas["Motor"].get_cantidad() == 10

    # agregar pieza que ya existe y que actualiza la cantidad
    operario.añadir_repuesto(Repuesto("Motor", "ProveedorA", 5, 1500.0), almacen)
    assert almacen.catalogo_piezas["Motor"].get_cantidad() == 15

    # actualización de precio
    operario.cambiar_precio_repuesto("Motor", 2000.0, almacen)
    assert almacen.catalogo_piezas["Motor"].precio == 2000.0

    # actualización de cantidad mediante el método reponer_repuesto
    operario.reponer_repuesto("Motor", 5, almacen)
    assert almacen.catalogo_piezas["Motor"].get_cantidad() == 20

    # el comandante adquiere repuesto
    comandante.adquirir_repuesto("Motor", 5, almacen)
    assert almacen.catalogo_piezas["Motor"].get_cantidad() == 15

    

def test_almacen_permisos_y_errores():
    almacen = Almacen("Almacen1", "Tatooine")
    operario = OperarioAlmacen("Op1")
    operario2 = OperarioAlmacen("Op2")
    nave = CazaEstelar("C1", ["Motor"], 4)
    comandante = Comandante("Com1", nave)

    almacen.añadir_operario(operario)
    almacen.añadir_comandante(comandante)

    rep = Repuesto("Motor", "ProveedorA", 10, 1500.0)
    operario.añadir_repuesto(rep, almacen)

    # no añadirmos al operario2 al almacen
    with pytest.raises(PermisoDenegadoError):
        almacen.añadir_repuesto(Repuesto("Ala", "ProveedorB", 5, 1200), operario2)

    # adquirir un repuesto que no existe
    with pytest.raises(ValueError):
        almacen.adquirir_repuesto("NoExiste", 1, comandante)

    # adquirir una cantidad negativa
    with pytest.raises(CantidadError):
        almacen.adquirir_repuesto("Motor", -1, comandante)

    # adquirir una cantidad mayor a la disponible
    with pytest.raises(CantidadError):
        almacen.adquirir_repuesto("Motor", 999, comandante)


def test_repuesto_validaciones():
    # crear repuesto con nombre vacio
    with pytest.raises(ValueError):
        Repuesto("", "Proveedor", 10, 50.0)
    # repuesto con proveedor vacio
    with pytest.raises(ValueError):
        Repuesto("Motor", "", 10, 50.0)
    # repuesto con cantidad negativa
    with pytest.raises(ValueError):
        Repuesto("Motor", "Proveedor", -1, 50.0)
    # repuesto con precio negativo
    with pytest.raises(ValueError):
        Repuesto("Motor", "Proveedor", 1, -1.0)

    r = Repuesto("Motor", "Proveedor", 10, 100.0)

    # añadir cantidad 0
    with pytest.raises(ValueError):
        r.añadir_cantidad(0)
    # reducir cantidad 0
    with pytest.raises(ValueError):
        r.reducir_cantidad(0)
    # cambiar a precio negativo
    with pytest.raises(ValueError):
        r.cambiar_precio(-10)

