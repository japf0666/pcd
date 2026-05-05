import pytest
from Imperio_Galactico import OperarioAlmacen, Usuario

# Creamos una clase concreta simple para probar Usuario directamente
class UsuarioPrueba(Usuario):
    def iniciarSesion(self) -> None:
        super().iniciarSesion()
    def cerrarSesion(self) -> None:
        super().cerrarSesion()

# --- TESTS ---

def test_usuario_creacion_correcta():
    """Verifica que un usuario se crea correctamente con strings."""
    user = UsuarioPrueba("1234", "Pablo")
    assert user._idUsuario == "1234"
    assert user._nombre == "Pablo"

def test_usuario_error_id_no_str():
    """Verifica TypeError si el idUsuario no es string."""
    with pytest.raises(TypeError, match="idUsuario debe ser una cadena de texto"):
        UsuarioPrueba(123, "Pablo")

def test_usuario_error_nombre_no_str():
    """Verifica TypeError si el nombre no es string."""
    with pytest.raises(TypeError, match="nombre debe ser una cadena de texto"):
        UsuarioPrueba("1234", ["Pablo"])

def test_operario_inicio_sesion_output(capsys):
    """Verifica que el inicio de sesión imprima el formato esperado."""
    operario = OperarioAlmacen("5678", "Sara")
    operario.iniciarSesion()
    
    captured = capsys.readouterr()
    # Comprobamos que sale el mensaje de la clase hija
    assert "Operario de Almacen Sara con id 5678 ha iniciado sesion" in captured.out

def test_operario_cerrar_sesion_output(capsys):
    """Verifica que el cierre de sesión imprima el formato esperado."""
    operario = OperarioAlmacen("5678", "Sara")
    operario.cerrarSesion()
    
    captured = capsys.readouterr()
    assert "Operario de Almacen Sara con id 5678 ha cerrado sesion" in captured.out

def test_usuario_es_abstracto():
    """Verifica que la clase Usuario no se puede instanciar por ser abstracta."""
    with pytest.raises(TypeError):
        Usuario("1357", "Juan")