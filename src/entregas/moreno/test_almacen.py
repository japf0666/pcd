
# Código de prueba utilizando pytest
# ============================

import pytest
from repuesto import Repuesto
from almacen import Almacen

# Test 1: Crear almacén y añadir repuestos
def test_añadir_repuesto():
    almacen = Almacen("Almacen Imperial", "Nebulosa Kaliida")
    r1 = Repuesto("Motor Hiperespacial", "Kuat Drive Yards", 10, 50000)
    almacen.añadir_repuesto(r1)

    # Verificar si el repuesto ha sido añadido correctamente
    assert len(almacen.catalogo) == 1
    assert almacen.catalogo[0].nombre == "Motor Hiperespacial"

# Test 2: Eliminar repuesto
def test_eliminar_repuesto():
    almacen = Almacen("Almacen Imperial", "Nebulosa Kaliida")
    r1 = Repuesto("Motor Hiperespacial", "Kuat Drive Yards", 10, 50000)
    almacen.añadir_repuesto(r1)

    # Eliminar el repuesto
    almacen.eliminar_repuesto("Motor Hiperespacial")

    # Verificar que el repuesto ha sido eliminado
    assert len(almacen.catalogo) == 0

# Test 3: Actualizar stock
def test_actualizar_stock():
    almacen = Almacen("Almacen Imperial", "Nebulosa Kaliida")
    r1 = Repuesto("Motor Hiperespacial", "Kuat Drive Yards", 10, 50000)
    almacen.añadir_repuesto(r1)

    # Aumentar stock
    almacen.actualizar_stock("Motor Hiperespacial", 5)
    assert r1.get_cantidad() == 15

    # Reducir stock
    almacen.actualizar_stock("Motor Hiperespacial", -3)
    assert r1.get_cantidad() == 12