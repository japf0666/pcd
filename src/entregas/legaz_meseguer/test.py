import pytest
import sys
import os

# Añadir el directorio base al path para importar los módulos desde src
sys.path.insert(0, os.path.dirname(__file__))

from src.logistica.repuesto import Repuesto
from src.logistica.almacen import Almacen
from src.usuarios.usuario import Usuario, Comandante, Opeario
from src.flota.unidad_combate_imperial import UnidadCombateImperial, Nave, EstacionEspacial, NaveEstelar
from src.utils.enumeraciones import Ubicacion, ClaseNaveEstelar

# Tests para la clase Repuesto
class TestRepuesto:
    def test_init(self):
        repuesto = Repuesto("Motor", "Proveedor1", 10, 100.0)
        assert repuesto.nombre == "Motor"
        assert repuesto.proveedor == "Proveedor1"
        assert repuesto.get_cantidad() == 10
        assert repuesto.precio == 100.0

    def test_get_cantidad(self):
        repuesto = Repuesto("Motor", "Proveedor1", 10, 100.0)
        assert repuesto.get_cantidad() == 10

    def test_set_cantidad_valida(self):
        repuesto = Repuesto("Motor", "Proveedor1", 10, 100.0)
        repuesto.set_cantidad(20)
        assert repuesto.get_cantidad() == 20

    def test_set_cantidad_negativa(self):
        repuesto = Repuesto("Motor", "Proveedor1", 10, 100.0)
        with pytest.raises(ValueError, match="Cantidad no puede ser negativa"):
            repuesto.set_cantidad(-5)

# Tests para la clase Almacen
class TestAlmacen:
    def test_init(self):
        almacen = Almacen("Almacen Central", "Base Imperial")
        assert almacen.nombre == "Almacen Central"
        assert almacen.localizacion == "Base Imperial"
        assert almacen.inventario == []

# Tests para la clase Usuario
class TestUsuario:
    def test_init(self):
        usuario = Usuario("Juan", "U001")
        assert usuario.nombre == "Juan"
        assert usuario.id_usuario == "U001"

# Tests para la clase Comandante
class TestComandante:
    def test_init(self):
        comandante = Comandante("Comandante Rex", "C001")
        assert comandante.nombre == "Comandante Rex"
        assert comandante.id_usuario == "C001"

    def test_consultar_repuesto_encontrado(self, capsys):
        almacen = Almacen("Almacen 1", "Loc1")
        repuesto = Repuesto("Motor", "Prov1", 5, 100.0)
        almacen.inventario.append(repuesto)
        comandante = Comandante("Rex", "C001")

        resultado = comandante.consultar_repuesto("Motor", almacen)
        assert resultado == repuesto

        captured = capsys.readouterr()
        assert "Comandante : Rex consultando en Almacén Almacen 1" in captured.out
        assert "Pieza encontrada : Motor | Stock: 5 | Precio: 100.0 créditos" in captured.out

    def test_consultar_repuesto_no_encontrado(self, capsys):
        almacen = Almacen("Almacen 1", "Loc1")
        comandante = Comandante("Rex", "C001")

        resultado = comandante.consultar_repuesto("Motor", almacen)
        assert resultado is None

        captured = capsys.readouterr()
        assert "La pieza Motor no esta disponible en este almacen" in captured.out

    def test_adquirir_repuesto_exitoso(self, capsys):
        almacen = Almacen("Almacen 1", "Loc1")
        repuesto = Repuesto("Motor", "Prov1", 5, 100.0)
        almacen.inventario.append(repuesto)
        comandante = Comandante("Rex", "C001")

        comandante.adquirir_repuesto("Motor", almacen)
        assert repuesto.get_cantidad() == 4

        captured = capsys.readouterr()
        assert "La pieza Motor ha sido comprada con exito" in captured.out

    def test_adquirir_repuesto_sin_stock(self, capsys):
        almacen = Almacen("Almacen 1", "Loc1")
        repuesto = Repuesto("Motor", "Prov1", 0, 100.0)
        almacen.inventario.append(repuesto)
        comandante = Comandante("Rex", "C001")

        comandante.adquirir_repuesto("Motor", almacen)
        assert repuesto.get_cantidad() == 0

        captured = capsys.readouterr()
        assert "No hay stock" in captured.out

# Tests para la clase Opeario
class TestOpeario:
    def test_init(self):
        opeario = Opeario("Operario Uno", "O001")
        assert opeario.nombre == "Operario Uno"
        assert opeario.id_usuario == "O001"

    def test_registrar_repuesto(self, capsys):
        almacen = Almacen("Almacen 1", "Loc1")
        repuesto = Repuesto("Motor", "Prov1", 10, 100.0)
        opeario = Opeario("Operario Uno", "O001")

        opeario.registrar_repuesto(repuesto, almacen)
        assert repuesto in almacen.inventario

        captured = capsys.readouterr()
        assert "Se ha registrado la pieza Motor en el almacen Almacen 1" in captured.out

    def test_actualizar_stock(self, capsys):
        repuesto = Repuesto("Motor", "Prov1", 10, 100.0)
        opeario = Opeario("Operario Uno", "O001")

        opeario.actualizar_stock(repuesto, 20)
        assert repuesto.get_cantidad() == 20

        captured = capsys.readouterr()
        assert "Operario Operario Uno ha actualizado el stock de Motor a 20" in captured.out

# Tests para las clases de flota
class TestUnidadCombateImperial:
    def test_init(self):
        unidad = UnidadCombateImperial("UC001", 12345)
        assert unidad.id_combate == "UC001"
        assert unidad.clave_transmision == 12345

class TestNave:
    def test_init(self):
        nave = Nave("N001", 12345, "Destructor Estelar")
        assert nave.id_combate == "N001"
        assert nave.clave_transmision == 12345
        assert nave.nombre == "Destructor Estelar"
        assert nave.catalogo_repuestos == []

class TestEstacionEspacial:
    def test_init(self):
        estacion = EstacionEspacial("E001", 12345, "Estacion Alpha", 100, 50, Ubicacion.ENDOR)
        assert estacion.id_combate == "E001"
        assert estacion.clave_transmision == 12345
        assert estacion.nombre == "Estacion Alpha"
        assert estacion.tripulacion == 100
        assert estacion.pasaje == 50
        assert estacion.ubicacion == Ubicacion.ENDOR

class TestNaveEstelar:
    def test_init(self):
        nave = NaveEstelar("NE001", 12345, "Eclipse", 500, 200, ClaseNaveEstelar.ECLIPSE)
        assert nave.id_combate == "NE001"
        assert nave.clave_transmision == 12345
        assert nave.nombre == "Eclipse"
        assert nave.tripulacion == 500
        assert nave.pasaje == 200
        assert nave.clase == ClaseNaveEstelar.ECLIPSE

# Tests para enumeraciones
class TestEnumeraciones:
    def test_ubicacion(self):
        assert Ubicacion.ENDOR.value == 'Endor'
        assert Ubicacion.CUMULO_RAIMOS.value == 'Cúmulo Raimos'
        assert Ubicacion.NEULOSSA.value == 'Nebulosa'
        assert Ubicacion.KALIIDA.value == 'Kaliida'

    def test_clase_nave_estelar(self):
        assert ClaseNaveEstelar.EJECTUR.value == 'Ejecturo'
        assert ClaseNaveEstelar.ECLIPSE.value == 'Eclipse'
        assert ClaseNaveEstelar.SOBREANO.value == 'Soberano'
    
