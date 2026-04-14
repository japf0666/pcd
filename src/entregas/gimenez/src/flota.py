# IMPORTACIONES
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

# EXCEPCIONES PERSONALIZADAS
class ExcepcionStockInsuficiente(Exception):
    """Excepción lanzada cuando se intenta adquirir más stock del disponible"""
    pass


# ENUMERACIONES
class Ubicacion(Enum):
    """Enumeración para representar las ubicaciones de las estaciones espaciales"""
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class ClaseNave(Enum):
    """Enumeración para representar las clases de naves estelares"""
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"


# 1. JERARQUÍA DE UNIDADES DE COMBATE
class UnidadCombate(ABC):
    """Clase abstracta base para todas las unidades de combate"""
    def __init__(self, identificador_combate: str, clave_transmision_cifrada: int):
        self.identificador_combate = identificador_combate
        self.clave_transmision_cifrada = clave_transmision_cifrada

class Nave(UnidadCombate):
    """Clase abstracta que representa una nave genérica"""
    def __init__(self, identificador_combate: str, clave_transmision_cifrada: int, nombre: str):
        super().__init__(identificador_combate, clave_transmision_cifrada) # Llamada al constructor de la clase base UnidadCombate
        self.nombre = nombre
        self.catalogo_repuestos: List[str] = []

class NaveTripulada(Nave):
    """Clase abstracta intermedia para naves con tripulación y pasaje"""
    def __init__(self, identificador_combate: str, clave_transmision_cifrada: int, nombre: str, tripulacion: int, pasaje: int):
        super().__init__(identificador_combate, clave_transmision_cifrada, nombre) # Llamada al constructor de la clase base Nave
        self.tripulacion = tripulacion
        self.pasaje = pasaje

class EstacionEspacial(NaveTripulada):
    """Clase concreta que representa una estación espacial con ubicación específica"""
    def __init__(self, identificador_combate: str, clave_transmision_cifrada: int, nombre: str, tripulacion: int, pasaje: int, ubicacion: Ubicacion):
        super().__init__(identificador_combate, clave_transmision_cifrada, nombre, tripulacion, pasaje) # Llamada al constructor de la clase base NaveTripulada
        self.ubicacion = ubicacion

class NaveEstelar(NaveTripulada):
    """Clase concreta que representa una nave estelar con clase específica"""
    def __init__(self, identificador_combate: str, clave_transmision_cifrada: int, nombre: str, tripulacion: int, pasaje: int, clase: ClaseNave):
        super().__init__(identificador_combate, clave_transmision_cifrada, nombre, tripulacion, pasaje) # Llamada al constructor de la clase base NaveTripulada
        self.clase = clase

class CazaEstelar(Nave):
    """Clase concreta que representa un caza estelar sin tripulación ni pasaje"""
    def __init__(self, identificador_combate: str, clave_transmision_cifrada: int, nombre: str, dotacion: int):
        super().__init__(identificador_combate, clave_transmision_cifrada, nombre) # Llamada al constructor de la clase base Nave
        self.dotacion = dotacion


# 2. SISTEMA DE INVENTARIO
class Repuesto:
    """Representa una pieza física en el inventario"""
    def __init__(self, nombre: str, proveedor: str, cantidad_disponible: int, precio: float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad_disponible = cantidad_disponible  # Atributo Privado (Encapsulamiento)
        self.precio = precio

    def get_cantidad_disponible(self) -> int:
        return self.__cantidad_disponible

    def set_cantidad_disponible(self, cantidad: int) -> None:
        if cantidad < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")
        self.__cantidad_disponible = cantidad

class Almacen:
    """Almacén físico que guarda un catálogo de repuestos"""
    def __init__(self, nombre: str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo_repuestos: List[Repuesto] = []


# 3. SISTEMA DE USUARIOS E INTERACCIONES
class Usuario(ABC):
    """Clase abstracta para los usuarios del sistema informático"""
    def __init__(self, nombre: str):
        self.nombre = nombre

class Comandante(Usuario):
    """Comandante de la flota, responsable de adquirir repuestos para las naves"""
    def consultar_repuestos(self, almacen: Almacen) -> List[Repuesto]:
        return almacen.catalogo_repuestos

    def adquirir_repuesto(self, almacen: Almacen, repuesto: Repuesto, cantidad: int) -> None:
        
        # Lógica definida en el Diagrama de Secuencia para la adquisición de repuestos
        if repuesto not in almacen.catalogo_repuestos:
            raise ValueError(f"El repuesto '{repuesto.nombre}' no se encuentra en este almacén.")
        
        cantidad_actual = repuesto.get_cantidad_disponible()
        
        # Bloque ALT del diagrama de secuencia
        if cantidad_actual >= cantidad:
            repuesto.set_cantidad_disponible(cantidad_actual - cantidad)
            print(f"Éxito: Se han adquirido {cantidad} unidades de '{repuesto.nombre}'. Disponibles restantes: {repuesto.get_cantidad_disponible()}.")
        else:
            raise ExcepcionStockInsuficiente(
                f"Stock insuficiente para '{repuesto.nombre}'. Solicitados: {cantidad}, Disponibles: {cantidad_actual}."
            )

class OperarioAlmacen(Usuario):
    """Operario del almacén, responsable de mantener el catálogo de repuestos y actualizar el stock"""
    def mantener_lista_repuestos(self, almacen: Almacen, repuesto: Repuesto, accion: str) -> None:
        if accion == "añadir":
            almacen.catalogo_repuestos.append(repuesto)
        elif accion == "eliminar" and repuesto in almacen.catalogo_repuestos:
            almacen.catalogo_repuestos.remove(repuesto)

    def actualizar_stock(self, almacen: Almacen, repuesto: Repuesto, cantidad: int) -> None:
        if repuesto in almacen.catalogo_repuestos:
            repuesto.set_cantidad_disponible(cantidad)