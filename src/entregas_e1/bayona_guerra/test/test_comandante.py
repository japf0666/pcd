import pytest
from Imperio_Galactico import Comandante, Usuario, Almacen, Repuesto, EmptyError, StockError

# Clase de apoyo para probar la abstracción de Usuario directamente 
class UsuarioPrueba(Usuario):
    def iniciarSesion(self) -> None:
        super().iniciarSesion()

    def cerrarSesion(self) -> None:
        super().cerrarSesion()

# --- TESTS ---

def test_usuario_creacion_error_tipos():
    """Verifica que el constructor de Usuario (vía Comandante) valide tipos."""
    with pytest.raises(TypeError, match="idUsuario debe ser una cadena de texto"):
        Comandante(123, "Pablo")
    
    with pytest.raises(TypeError, match="nombre debe ser una cadena de texto"):
        Comandante("123", 456)

def test_comandante_inicializacion_diccionario():
    """Verifica que el Comandante inicie con el diccionario de repuestos vacío."""
    Pablo = Comandante("456", "Pablo")
    # Accedemos al atributo protegido para verificar que es un diccionario vacío
    assert isinstance(Pablo._repuestosSolicitados, dict)
    assert len(Pablo._repuestosSolicitados) == 0

def test_comandante_sesion_mensajes(capsys):
    """Verifica los mensajes de inicio y cierre de sesión."""
    Pablo = Comandante("456", "Pablo")
    
    Pablo.iniciarSesion()
    out_inicio = capsys.readouterr().out
    assert "Comandante Pablo con id 456 ha iniciado sesion" in out_inicio

    Pablo.cerrarSesion()
    out_cierre = capsys.readouterr().out
    assert "Comandante Pablo con id 456 ha cerrado sesion" in out_cierre

def test_comandante_consultar_repuesto(capsys):
    """Verifica la búsqueda de repuestos en un almacén."""
    repuesto = Repuesto("Motor", "Mercadona", 10, 100.0)
    almacen = Almacen("Almacen1", "Endor", [repuesto])
    Pablo = Comandante("456", "Pablo")

    # Caso: Existe
    assert Pablo.consultarRepuesto("Motor", almacen) is True
    
    # Caso: No existe
    assert Pablo.consultarRepuesto("Laser", almacen) is False

def test_comandante_solicitar_repuesto_exito():
    """Verifica que se añadan repuestos al diccionario interno."""
    repuesto = Repuesto("Motor", "Mercadona", 10, 100.0)
    almacen = Almacen("Almacen1", "Endor", [repuesto])
    Pablo = Comandante("456", "Pablo")

    Pablo.solicitarRepuesto(repuesto, almacen, 2)
    assert Pablo._repuestosSolicitados["Motor"] == 2

def test_comandante_solicitar_repuesto_error_stock():
    """Verifica error si se pide un repuesto que no está en el almacén."""
    repuesto_en_almacen = Repuesto("Motor", "Mercadona", 10, 100.0)
    repuesto_no_en_almacen = Repuesto("Turbina", "Carrefour", 5, 50.0)
    almacen = Almacen("Almacen1", "Endor", [repuesto_en_almacen])
    Pablo = Comandante("456", "Pablo")

    with pytest.raises(StockError, match="NO se encuentra en stock"):
        Pablo.solicitarRepuesto(repuesto_no_en_almacen, almacen, 1)

def test_comandante_realizar_pedido_vacio():
    """Verifica error al realizar pedido sin haber solicitado nada antes."""
    almacen = Almacen("Almacen1", "Endor", [])
    Pablo = Comandante("456", "Pablo")

    with pytest.raises(EmptyError, match="lista de repuestos solicitados esta vacia"):
        Pablo.realizarPedido(almacen)

def test_comandante_realizar_pedido_exito():
    """Verifica que el pedido limpie la lista del comandante tras el éxito."""
    repuesto = Repuesto("Motor", "Mercadona", 10, 100.0)
    almacen = Almacen("Almacen1", "Endor", [repuesto])
    Pablo = Comandante("456", "Pablo")

    Pablo.solicitarRepuesto(repuesto, almacen, 1)
    Pablo.realizarPedido(almacen)

    # El diccionario debe quedar vacío tras el pedido
    assert len(Pablo._repuestosSolicitados) == 0