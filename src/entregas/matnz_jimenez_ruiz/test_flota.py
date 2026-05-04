# importamos paquetes necesarios para las pruebas
import pytest
from flota import CazaEstelar, Repuesto, StockInsuficienteError

def test_instanciacion_caza(): # prueba la creación de un objeto CazaEstelar y verifica sus atributos
    caza = CazaEstelar("TIE Interceptor", ["Láser doble"], 1, "TIE-INT", 777) #añadimos los atributos
    assert caza.nombre == "TIE Interceptor" #verificamos que el nombre del caza sea correcto
    assert caza.catalogo_repuestos == ["Láser doble"] #verificamos que el catálogo de repuestos sea correcto
    assert caza. id_combate == "TIE-INT" #verificamos que el ID de combate sea correcto

def test_extraccion_repuesto_exito(): # prueba para una pieza de repuesto
    motor = Repuesto("Motor Iónico", "Proveedor A", 10, 5000) #añadimos los atributos
    assert motor.extraer_repuesto(4) #verificamos que la extracción sea exitosa
    assert motor.cantidad == 6 #verificamos que la cantidad sea correcta

def test_extrraccion_repuesto_excepcion(): # prueba para una pieza de repuesto con error
    motor = Repuesto("Motor Iónico", "Proveedor A", 2, 5000) #añadimos los atributos
    with pytest.raises(StockInsuficienteError): # controlamos la excepcion de error que se espera que se lance
        motor.extraer_repuesto(5) # se intenta extraer una cantidad mayor a la disponible, lo que debería lanzar una excepción de stock insuficiente