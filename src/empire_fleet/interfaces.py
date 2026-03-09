from abc import ABC, abstractmethod


class InterfazConsultaRepuestos(ABC):
    """
    Interfaz segregada para clientes que solo consultan/compran repuestos.
    """

    @abstractmethod
    def consultar_repuestos_disponibles(self, almacen: object) -> list[object]:
        pass

    @abstractmethod
    def solicitar_repuesto(self, almacen: object, nombre_repuesto: str, cantidad: int) -> str:
        pass


class InterfazGestionInventario(ABC):
    """
    Interfaz segregada para usuarios que mantienen el inventario.
    """

    @abstractmethod
    def alta_repuesto(self, repuesto: object) -> None:
        pass

    @abstractmethod
    def eliminar_repuesto(self, nombre_repuesto: str) -> None:
        pass

    @abstractmethod
    def reponer_stock(self, nombre_repuesto: str, cantidad: int) -> None:
        pass


class UnidadCombate(ABC):
    """
    Abstracción para cualquier unidad de combate imperial.
    """

    def __init__(self, identificador_combate: str, clave_transmision: int) -> None:
        self.identificador_combate: str = identificador_combate
        self.clave_transmision: int = clave_transmision

    def transmitir_mensaje_cifrado(self, mensaje: str) -> str:
        return f"[{self.identificador_combate}] {mensaje} :: clave={self.clave_transmision}"


class Nave(ABC):
    """
    Abstracción base para todas las naves.
    """

    def __init__(self, nombre: str, catalogo_repuestos: list[str]) -> None:
        self.nombre: str = nombre
        self.catalogo_repuestos: list[str] = list(catalogo_repuestos)

    def consultar_catalogo(self) -> list[str]:
        return list(self.catalogo_repuestos)

    def admite_repuesto(self, nombre_repuesto: str) -> bool:
        return nombre_repuesto in self.catalogo_repuestos

    @abstractmethod
    def descripcion(self) -> str:
        pass