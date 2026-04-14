import pytest
from Imperio_Galactico import Usuario

# Creamos una clase concreta para poder testear la clase abstracta
class UsuarioPrueba(Usuario):
    def iniciarSesion(self) -> None:
        print(f"Sesión iniciada para {self._nombre}")

    def cerrarSesion(self) -> None:
        print(f"Sesión cerrada para {self._nombre}")

# --- TESTS ---

def test_usuario_creacion_correcta():
    """Verifica que un usuario se crea correctamente con tipos válidos."""
    u = UsuarioPrueba("1234", "Pablo")
    assert u._idUsuario == "1234"
    assert u._nombre == "Pablo"

def test_usuario_error_id_no_str():
    """Verifica TypeError si el idUsuario no es string."""
    with pytest.raises(TypeError, match="idUsuario debe ser una cadena de texto"):
        UsuarioPrueba(123, "Pablo")

def test_usuario_error_nombre_no_str():
    """Verifica TypeError si el nombre no es string."""
    with pytest.raises(TypeError, match="nombre debe ser una cadena de texto"):
        UsuarioPrueba("1234", ["Pablo"])

def test_usuario_metodos_sesion(capsys):
    """Verifica que los métodos de sesión funcionan en la clase hija."""
    u = UsuarioPrueba("1234", "Pablo")
    
    u.iniciarSesion()
    captured = capsys.readouterr()
    assert "Sesión iniciada para Pablo" in captured.out

    u.cerrarSesion()
    captured = capsys.readouterr()
    assert "Sesión cerrada para Pablo" in captured.out

def test_usuario_es_abstracto():
    """Verifica que no se puede instanciar la clase Usuario directamente."""
    with pytest.raises(TypeError):
        Usuario("5678", "Sara")