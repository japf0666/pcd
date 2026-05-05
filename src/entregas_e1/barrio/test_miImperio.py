import pytest
from miImperio import Repuesto, Almacen, Comandante, Estacion_Espacial
@pytest.fixture
def almacen_con_motor():
    almacen = Almacen("Base A", "Endor")
    motor = Repuesto("Motor", "Pedro", 1, 500.0)
    almacen.añadir_repuesto(motor)
    return almacen

@pytest.fixture
def comandante_paco():
    return Comandante("Paco")

# 1. Test de creacion correcta
def test_crear_repuesto_correcto():
    motor = Repuesto("Motor", "Pedro", 5, 500.0)
    assert motor.nombre == "Motor"
    assert motor.get_cantidad() == 5

# 2. Test de TypeError 
def test_crear_repuesto_error_tipo():
    with pytest.raises(TypeError):
        Repuesto("Tornillo", "Pedro", "cinco", 10.5)

# 3. Test de ValueError 
def test_crear_estacion_error_ubicacion():
    with pytest.raises(ValueError):
        Estacion_Espacial("0987", 1234, "EEI", ["Tornillo"], 100, 10, "Marte")

# 4. Test de compra exitosa
def test_comandante_adquirir_exito(almacen_con_motor, comandante_paco):
    comandante_paco.adquirir_repuesto(almacen_con_motor, "Motor")
    # El stock debe bajar a 0 despues de la compra
    assert almacen_con_motor.repuestos[0].get_cantidad() == 0

# 5. Test de compra sin stock
def test_comandante_adquirir_sin_stock(almacen_con_motor, comandante_paco):
    almacen_con_motor.repuestos[0].set_cantidad(0) 
    comandante_paco.adquirir_repuesto(almacen_con_motor, "Motor")
    # El stock debe mantenerse en 0, no en negativo
    assert almacen_con_motor.repuestos[0].get_cantidad() == 0