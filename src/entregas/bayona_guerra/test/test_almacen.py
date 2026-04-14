import pytest
from Imperio_Galactico import Usuario

# Creamos una clase concreta para poder probar la clase abstracta Usuario
class UsuarioPrueba(Usuario):
    def iniciarSesion(self) -> None:
        print(f"Sesión iniciada para {self._nombre}")

    def cerrarSesion(self) -> None:
        print(f"Sesión cerrada para {self._nombre}")

# --- TESTS ---

def test_usuario_creacion_correcta():
    """Verifica que un usuario se cree correctamente con datos válidos."""
    user = UsuarioPrueba("12345", "Pablo")
    assert user._idUsuario == "12345"
    assert user._nombre == "Pablo"

def test_usuario_error_id_no_str():
    """Verifica TypeError si el idUsuario no es un string."""
    with pytest.raises(TypeError, match="idUsuario debe ser una cadena de texto"):
        UsuarioPrueba(123, "Pablo")

def test_usuario_error_nombre_no_str():
    """Verifica TypeError si el nombre no es un string."""
    with pytest.raises(TypeError, match="nombre debe ser una cadena de texto"):
        UsuarioPrueba("12345", ["Pablo"])

def test_usuario_metodos_abstractos(capsys):
    """Verifica que los métodos implementados en la subclase funcionen."""
    user = UsuarioPrueba("12345", "Pablo")
    
    user.iniciarSesion()
    captured = capsys.readouterr()
    assert "Sesión iniciada para Pablo" in captured.out
    
    user.cerrarSesion()
    captured = capsys.readouterr()
    assert "Sesión cerrada para Pablo" in captured.out

def test_usuario_es_abstracto():
    """Verifica que no se pueda crear la clase Usuario directamente."""
    with pytest.raises(TypeError):
        Usuario("BASE-01", "Invalido")