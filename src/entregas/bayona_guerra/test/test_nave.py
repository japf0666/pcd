import pytest
from Imperio_Galactico import Nave, Repuesto, EmptyError, RepuestoInexistente

# Clase de apoyo (debe coincidir con la firma de UnidadCombate)
class NavePrueba(Nave):
    def transmitirMensaje(self, mensaje: str, clave: int) -> None:
        pass

# --- TESTS ---

def test_consultar_catalogo_con_piezas():
    mi_nave = NavePrueba("1234", 123, "Nave", ["Motor", "Laser"])
    resultado = mi_nave.consultarCatalogo()
    assert "Motor" in resultado
    assert len(resultado) == 2

def test_solicitar_repuesto_existente():
    mi_nave = NavePrueba("1234", 123, "Nave", ["Motor"])
    mi_repuesto = Repuesto("Motor", "Mercadona", 10, 500.0)
    
    # Como la función devuelve None, no guardamos el resultado en una variable 'exito'
    mi_nave.solicitarRepuesto(mi_repuesto, 5)
    
    # Comprobamos que el stock ha bajado de 10 a 5. 
    # Si esto es cierto, es que la función se ejecutó correctamente hasta el final.
    assert mi_repuesto.obtenerUnidades() == 5

def test_solicitar_repuesto_no_en_catalogo():
    mi_nave = NavePrueba("1234", 123, "Nave", ["Motor"])
    repuesto_erroneo = Repuesto("Escudo", "Carrefour", 10, 100.0)
    
    # Verificamos que se lanza la excepción correcta
    with pytest.raises(RepuestoInexistente):
        mi_nave.solicitarRepuesto(repuesto_erroneo, 1)