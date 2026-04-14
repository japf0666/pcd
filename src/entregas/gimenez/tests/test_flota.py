# IMPORTACIONES
import pytest
import sys
import os

# Ajuste del path para que pytest encuentre la carpeta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from flota import (
    Ubicacion, EstacionEspacial, Repuesto, Almacen, 
    Comandante, OperarioAlmacen, ExcepcionStockInsuficiente
)

# FIXTURES (Datos de prueba reutilizables)
@pytest.fixture
def almacen_prueba():
    """Crea un almacén vacío para usar en los tests"""
    return Almacen(
        nombre="Almacén Test", 
        localizacion="Tatooine"
    )

@pytest.fixture
def repuesto_prueba():
    """Crea un repuesto con 10 unidades de stock"""
    return Repuesto(
        nombre="Motor Hiperimpulsor",
        proveedor="Kuat Drive Yards",
        cantidad_disponible=10,
        precio=5000.0
    )


# TESTS UNITARIOS

def test_creacion_estacion_espacial():
    """Verifica que la herencia y los atributos de las naves se asignan correctament."""
    
    # Creamos una estación espacial y verificamos sus atributos
    estacion = EstacionEspacial(
        identificador_combate="EST-1", 
        clave_transmision_cifrada=999, 
        nombre="Estación de Prueba", 
        tripulacion=100, 
        pasaje=50, 
        ubicacion=Ubicacion.ENDOR
    )
    assert estacion.nombre == "Estación de Prueba" # Atributo heredado de NaveTripulada
    assert estacion.ubicacion == Ubicacion.ENDOR # Atributo específico de EstacionEspacial
    assert estacion.tripulacion == 100 # Atributo heredado de NaveTripulada


def test_operario_añade_repuesto(almacen_prueba, repuesto_prueba):
    """Verifica que un operario puede modificar el catálogo del almacén"""
    
    # Creamos un operario y añadimos un repuesto al almacén
    operario = OperarioAlmacen(
        nombre="TK-Test"
    )
    # Añadimos el repuesto al almacén usando el método del operario
    operario.mantener_lista_repuestos(
        almacen=almacen_prueba, 
        repuesto=repuesto_prueba, 
        accion="añadir"
    )

    assert len(almacen_prueba.catalogo_repuestos) == 1 # El repuesto se ha añadido al catálogo
    assert almacen_prueba.catalogo_repuestos[0].nombre == "Motor Hiperimpulsor" # El repuesto añadido es el correcto


def test_comandante_compra_con_exito(almacen_prueba, repuesto_prueba):
    """Verifica que la compra descuenta el stock correctamente si hay cantidad suficiente."""
    
    # Primero añadimos el repuesto al almacén para que el comandante pueda comprarlo
    operario = OperarioAlmacen(
        nombre="TK-Test"
    )
    # Añadimos el repuesto al almacén usando el método del operario
    operario.mantener_lista_repuestos(
        almacen=almacen_prueba,
        repuesto=repuesto_prueba,
        accion="añadir"
    )
    # Añadimos el repuesto al almacén para que el comandante pueda comprarlo
    comandante = Comandante(
        nombre="Comandante Test"
    )
    # Compramos 3 unidades (hay 10 disponibles)
    comandante.adquirir_repuesto(
        almacen=almacen_prueba, 
        repuesto=repuesto_prueba, 
        cantidad=3
    )

    assert repuesto_prueba.get_cantidad_disponible() == 7 # El stock se ha reducido de 10 a 7

def test_comandante_excepcion_stock(almacen_prueba, repuesto_prueba):
    """Verifica que salta la excepción personalizada al pedir más stock del disponible"""
    # Primero añadimos el repuesto al almacén para que el comandante pueda comprarlo
    operario = OperarioAlmacen(
        nombre="TK-Test"
    )
    # Añadimos el repuesto al almacén usando el método del operario
    operario.mantener_lista_repuestos(
        almacen=almacen_prueba,
        repuesto=repuesto_prueba,
        accion="añadir"
    )
    # Añadimos el repuesto al almacén para que el comandante pueda comprarlo
    comandante = Comandante(
        nombre="Comandante Test"
    )
    # Intentamos comprar 15 cuando solo hay 10. Tiene que saltar la excepción.
    with pytest.raises(ExcepcionStockInsuficiente):
        comandante.adquirir_repuesto(
            almacen=almacen_prueba,
            repuesto=repuesto_prueba,
            cantidad=15
        )