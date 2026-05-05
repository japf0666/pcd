from enum import Enum
from abc import ABC, abstractmethod

# EXCEPCIONES 

class StockInsuficienteError(Exception):
    pass

class RepuestoNoEncontradoError(Exception):
    pass

# ENUMERACIONES 

class Ubicacion(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class ClaseNave(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

#CLASES ABSTRACTAS 

class UnidadCombate(ABC):
    def __init__(self, id_combate: str, clave_cifrada: int):
        self._id_combate = id_combate
        self._clave_cifrada = clave_cifrada

class Nave(ABC):
    def __init__(self, nombre: str, catalogo_repuestos: list):
        self._nombre = nombre
        self._catalogo_repuestos = catalogo_repuestos

    @abstractmethod
    def descripcion(self) -> str:
        pass

#SUBCLASES CONCRETAS

class EstacionEspacial(Nave):
    def __init__(self, nombre: str, catalogo_repuestos: list,tripulacion: int, pasaje: int, ubicacion: Ubicacion):
        super().__init__(nombre, catalogo_repuestos)
        self._tripulacion = tripulacion
        self._pasaje = pasaje
        self._ubicacion = ubicacion

    def descripcion(self) -> str:
        return (f"[EstacionEspacial] {self._nombre} | "
                f"Tripulación: {self._tripulacion} | "
                f"Pasaje: {self._pasaje} | "
                f"Ubicación: {self._ubicacion.value}")


class NaveEstelar(Nave):
    def __init__(self, nombre: str, catalogo_repuestos: list,tripulacion: int, pasaje: int, clase: ClaseNave):
        super().__init__(nombre, catalogo_repuestos)
        self._tripulacion = tripulacion
        self._pasaje = pasaje
        self._clase = clase

    def descripcion(self) -> str:
        return (f"[NaveEstelar] {self._nombre} | "
                f"Clase: {self._clase.value} | "
                f"Tripulación: {self._tripulacion} | "
                f"Pasaje: {self._pasaje}")


class CazaEstelar(Nave, UnidadCombate):
    def __init__(self, nombre: str, catalogo_repuestos: list,dotacion: int, id_combate: str, clave_cifrada: int):
        Nave.__init__(self, nombre, catalogo_repuestos)
        UnidadCombate.__init__(self, id_combate, clave_cifrada)
        self._dotacion = dotacion

    def descripcion(self) -> str:
        return (f"[CazaEstelar] {self._nombre} | "
                f"Dotación: {self._dotacion} | "
                f"ID Combate: {self._id_combate} | "
                f"Clave Cifrada: {self._clave_cifrada}")

# REPUESTO Y ALMACEN 

class Repuesto:
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad    # atributo PRIVADO
        self.precio = precio

    def get_cantidad(self) -> int:
        return self.__cantidad

    def añadir_stock(self, cantidad: int):
        self.__cantidad += cantidad

    def consumir_stock(self, cantidad: int):
        if cantidad > self.__cantidad:
            raise StockInsuficienteError(
                f"Stock insuficiente para '{self.nombre}': "
                f"disponible={self.__cantidad}, solicitado={cantidad}."
            )
        self.__cantidad -= cantidad

    def __str__(self) -> str:
        return (f"Repuesto('{self.nombre}', proveedor='{self.proveedor}', "
                f"stock={self.__cantidad}, precio={self.precio}€)")


class Almacen:
    def __init__(self, nombre: str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self._catalogo = []

    def agregar_repuesto(self, repuesto: Repuesto):
        self._catalogo.append(repuesto)

    def buscar_repuesto(self, nombre: str) -> Repuesto:
        for repuesto in self._catalogo:
            if repuesto.nombre == nombre:
                return repuesto
        raise RepuestoNoEncontradoError(f"El repuesto '{nombre}' no está en el almacén '{self.nombre}'.")

    def listar_catalogo(self):
        print(f"\n=== Catálogo de '{self.nombre}' ({self.localizacion}) ===")
        for r in self._catalogo:
            print(f"  {r}")
    
    # PRUEBA DEL CODIGO

if __name__ == "__main__":

    # Crear naves
    estacion = EstacionEspacial(
        "Estrella de la Muerte II",
        ["Turbolaser", "Generador de escudo"],
        485000, 38000,
        Ubicacion.ENDOR
    )
    print(estacion.descripcion())

    nave = NaveEstelar(
        "Devastador",
        ["Motor ion", "Escudo deflector"],
        37085, 9700,
        ClaseNave.EJECUTOR
    )
    print(nave.descripcion())

    caza = CazaEstelar(
        "TIE Advanced x1",
        ["Panel solar", "Cañón laser"],
        1, "TIE-ADV-001", 88421
    )
    print(caza.descripcion())

    # Crear almacén y repuestos
    almacen = Almacen("Almacén Orbital Delta", "Endor")
    almacen.agregar_repuesto(Repuesto("Motor ion", "Sienar Fleet", 50, 1200.0))
    almacen.agregar_repuesto(Repuesto("Panel solar", "Kuat Drive", 200, 450.0))
    almacen.listar_catalogo()

    # Prueba excepción StockInsuficienteError
    try:
        almacen.buscar_repuesto("Motor ion").consumir_stock(999)
    except StockInsuficienteError as e:
        print(f"\nCAPTURADO: {e}")

    # Prueba excepción RepuestoNoEncontradoError
    try:
        almacen.buscar_repuesto("Sable de luz")
    except RepuestoNoEncontradoError as e:
        print(f"CAPTURADO: {e}")