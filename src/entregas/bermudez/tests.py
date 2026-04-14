import pytest

from entregable1 import (
    Repuesto,
    Almacen,
    Comandante,
    Operario,
    Estacion_Espacial,
    Nave,
    Nave_Estelar,
    Caza_Estelar,
    Unidad_Combate,
    Usuario,
    Ubicacion,
    Clase,
)


def test_repuesto_precios_y_disponibilidad():
    """Verifica cálculos de precio total, disponibilidad y validaciones de repuestos."""
    rep = Repuesto("Motor", "Proveedor", stock=5, precio=10.0)

    assert rep.precio_total(3) == 30.0
    assert rep.es_disponible(5) is True
    assert rep.es_disponible(6) is False

    rep.actualizar_precio(12.5)
    assert rep.precio == 12.5

    with pytest.raises(ValueError):
        rep.precio_total(0)

    with pytest.raises(ValueError):
        rep.es_disponible(0)

    with pytest.raises(ValueError):
        rep.actualizar_precio(0)


def test_almacen_inventario_y_busquedas():
    """Verifica inventario, búsquedas por proveedor y eliminación en almacén."""
    rep1 = Repuesto("A", "P1", stock=3, precio=5.0)
    rep2 = Repuesto("B", "P2", stock=2, precio=6.0)
    almacen = Almacen("Alma", "Lugar", catalogo=[rep1, rep2])

    assert almacen.inventario() == {"A": 3, "B": 2}
    assert almacen.buscar_por_proveedor("P1") == [rep1]
    assert almacen.buscar_por_proveedor("X") == []

    assert almacen.eliminar_repuesto("A") is True
    assert almacen.buscar_repuesto("A") is None
    assert almacen.eliminar_repuesto("A") is False


def test_comandante_comparar_precios():
    """Verifica comparación de precios entre almacenes para un repuesto."""
    rep_a1 = Repuesto("RepuestoX", "P", stock=5, precio=100.0)
    rep_a2 = Repuesto("RepuestoX", "P", stock=5, precio=80.0)

    almac1 = Almacen("A1", "L1", catalogo=[rep_a1])
    almac2 = Almacen("A2", "L2", catalogo=[rep_a2])

    comandante = Comandante("Leia", Estacion_Espacial("Out", "EST-1", 1, 1, 1, Ubicacion.Endor))
    resultado = comandante.comparar_precios("RepuestoX", [almac1, almac2])

    assert resultado is not None
    almacen_mas_barato, precio = resultado
    assert almacen_mas_barato is almac2
    assert precio == 80.0

    assert comandante.comparar_precios("NoExiste", [almac1, almac2]) is None


def test_creacion_y_str_unidad_y_nave():
    """Verifica creación y representación string de Unidad_Combate y Nave."""
    u = Unidad_Combate("ID-1", 42)
    assert "ID-1" in str(u)

    n = Nave("Falcon", "ID-2", 99)
    assert "Falcon" in str(n)
    assert n.piezas_repuesto == []


def test_clases_de_naves_especializadas_y_str():
    """Verifica creación y representaciones de Estacion_Espacial, Nave_Estelar y Caza_Estelar."""
    est = Estacion_Espacial("Outpost", "EST-1", 1, tripulacion=10, pasaje=5, ubicacion=Ubicacion.Endor)
    assert "Outpost" in str(est)
    assert est.tripulacion == 10

    ne = Nave_Estelar("Enterprise", "NES-1", 2, tripulacion=100, pasaje=50, clase=Clase.Ejecutor)
    assert "Enterprise" in str(ne)
    assert ne.clase == Clase.Ejecutor

    ce = Caza_Estelar("Interceptor", "CZA-1", 3, dotacion=2)
    assert "Interceptor" in str(ce)
    assert ce.dotacion == 2


def test_usuarios_operaciones_basicas():
    """Verifica operaciones básicas que realizan operarios y comandantes sobre el almacén."""
    almacen = Almacen("Alma", "Lugar")
    ope = Operario("Juan", almacen)
    assert "Juan" in str(ope)

    rep = Repuesto("Pieza", "Prov", stock=1, precio=10.0)
    ope.añadir_repuesto(rep)
    assert almacen.buscar_repuesto("Pieza") is rep

    # Cambiar stock sube y baja
    ope.cambiar_stock("Pieza", 2)
    assert rep.get_disponibles() == 3
    ope.cambiar_stock("Pieza", -1)
    assert rep.get_disponibles() == 2

    # Comandante consulta y adquiere
    com = Comandante("Leia", Estacion_Espacial("Out", "EST-1", 1, 1, 1, Ubicacion.Endor))
    com.consultar_disponibilidad("Pieza", almacen)
    com.adquirir_repuesto("Pieza", almacen, 1)
    assert rep.get_disponibles() == 1

