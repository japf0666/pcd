"""Sistema de gestión de mantenimiento espacial.

Contiene clases para representar unidades de combate, naves, repuestos, almacenes y usuarios
(con comandantes y operarios) con operaciones de búsqueda, stock, comparaciones y más.
"""

from abc import ABC, abstractmethod
from enum import Enum

class Unidad_Combate:
    """Representa una unidad de combate base en la flota."""

    def __init__(self, id_combate: str, c_transmision: int):
        self.id_combate = id_combate
        self.c_transmision = c_transmision

    def __str__(self):
        return f"Unidad de Combate {self.id_combate} (transmisión={self.c_transmision})"

class Nave(Unidad_Combate):
    """Representa una nave genérica con nombre y piezas de repuesto."""

    def __init__(self, nombre: str, id_combate: str, c_transmision: int):
        super().__init__(id_combate, c_transmision)
        self.nombre = nombre
        self.piezas_repuesto = []

    def __str__(self):
        return f"Nave {self.nombre} [{self.id_combate}] - Transmisión {self.c_transmision}"

class Ubicacion(Enum):
    Endor = 1
    Cúmulo_Raimos = 2
    Nebulosa_Kaliida = 3

class Clase(Enum):
    Ejecutor = 1
    Eclipse = 2
    Soberano = 3

class Estacion_Espacial(Nave):
    """Nave especializada en funciones de estación espacial con tripulación y pasaje."""

    def __init__(self, nombre: str, id_combate: str, c_transmision: int, tripulacion: int, pasaje: int, ubicacion: Ubicacion):
        super().__init__(nombre, id_combate, c_transmision)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def __str__(self):
        return (f"Estación Espacial {self.nombre} [{self.id_combate}] - "
                f"Ubicación: {self.ubicacion.name}, Tripulación: {self.tripulacion}, Pasaje: {self.pasaje}")

class Nave_Estelar(Nave):
    """Nave de combate estelar con clase, tripulación y pasaje."""

    def __init__(self, nombre: str, id_combate: str, c_transmision: int, tripulacion: int, pasaje: int, clase: Clase):
        super().__init__(nombre, id_combate, c_transmision)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def __str__(self):
        return (f"Nave Estelar {self.nombre} [{self.id_combate}] - Clase: {self.clase.name}, "
                f"Tripulación: {self.tripulacion}, Pasaje: {self.pasaje}")


class Caza_Estelar(Nave):
    """Nave caza ligera con dotación mínima."""

    def __init__(self, nombre: str, id_combate: str, c_transmision: int, dotacion: int):
        super().__init__(nombre, id_combate, c_transmision)
        self.dotacion = dotacion

    def __str__(self):
        return f"Caza Estelar {self.nombre} [{self.id_combate}] - Dotación: {self.dotacion}"

class Repuesto:
    """Modelo de repuesto con control de stock, precio y proveedor."""

    def __init__(self, nombre: str, proveedor: str, stock: int, precio: float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__stock = stock
        self.precio = precio

    def get_disponibles(self) -> int:
        return self.__stock

    def precio_total(self, cantidad: int) -> float:
        """Calcula el precio total para una cantidad solicitada."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        return self.precio * cantidad

    def es_disponible(self, cantidad: int) -> bool:
        """Comprueba si hay stock suficiente para una cantidad dada."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        return self.__stock >= cantidad

    def actualizar_precio(self, nuevo_precio: float):
        """Actualiza el precio unitario del repuesto."""
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        self.precio = nuevo_precio

    def agregar_stock(self, n):
        """Aumenta el stock disponible sumando la cantidad n."""
        try:
            if n < 0:
                raise ValueError("No se puede agregar stock negativo")
            self.__stock += n
        except TypeError:
            print("Error: la cantidad a agregar debe ser un número")
        except ValueError as e:
            print(f"Error: {e}")

    def retirar_stock(self, n):
        """Reduce stock restando la cantidad n si hay suficiente disponible."""
        try:
            if n < 0:
                raise ValueError("No se puede retirar cantidad negativa")
            if (self.__stock - n) >= 0:
                self.__stock -= n
            else:
                raise ValueError("No hay suficiente stock para retirar")
        except TypeError:
            print("Error: la cantidad a retirar debe ser un número")
        except ValueError as e:
            print(f"Error: {e}")

    def __str__(self) -> str:
        return f"Repuesto: {self.nombre} | Proveedor: {self.proveedor} | Stock: {self.get_disponibles()} | Precio: {self.precio} cr"

class Almacen:
    """Representa un almacén donde se guarda un catálogo de repuestos."""

    def __init__(self, nombre: str, localizacion: str, catalogo: list[Repuesto] = None):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo = catalogo if catalogo is not None else []

    def __str__(self):
        return f"Almacén {self.nombre} ({self.localizacion}) - {len(self.catalogo)} repuestos"

    def buscar_repuesto(self, nom) -> Repuesto:
        """Busca un repuesto por nombre y devuelve el objeto Repuesto o None si no existe."""
        for repuesto in self.catalogo:
            if repuesto.nombre == nom:
                return repuesto
        return None

    def inventario(self) -> dict:
        """Devuelve un diccionario {nombre_repuesto: stock} para todo el catálogo."""
        return {r.nombre: r.get_disponibles() for r in self.catalogo}

    def buscar_por_proveedor(self, proveedor: str) -> list[Repuesto]:
        """Busca todos los repuestos de un proveedor dado."""
        return [r for r in self.catalogo if r.proveedor == proveedor]

    def eliminar_repuesto(self, nombre: str) -> bool:
        """Elimina un repuesto por nombre. Devuelve True si se eliminó, False si no existía."""
        for i, repuesto in enumerate(self.catalogo):
            if repuesto.nombre == nombre:
                del self.catalogo[i]
                return True
        return False

    def mostrar_catalogo(self):
        """Imprime el listado de repuestos en el catálogo."""
        for repuesto in self.catalogo:
            print(repuesto)

    def agregar_catalogo(self, repuesto: Repuesto):
        """Añade un repuesto al catálogo del almacén."""
        self.catalogo.append(repuesto)


class Usuario(ABC):
    """Usuario genérico de sistema con nombre de usuario."""

    def __init__(self, usuario: str):
        self.usuario = usuario

    @abstractmethod
    def __str__(self):
        pass

class Comandante(Usuario):
    """Usuario con capacidad de consultar y adquirir repuestos para una nave."""

    def __init__(self, usuario: str, nave: Nave):
        super().__init__(usuario)
        self.nave = nave

    def __str__(self):
        return f"Comandante {self.usuario} (Nave: {self.nave.nombre})"

    def consultar_disponibilidad(self, nombre_repuesto: str, almacen: Almacen):
        """Imprime la disponibilidad de un repuesto en un almacén."""
        repuesto = almacen.buscar_repuesto(nombre_repuesto)

        if repuesto is not None:
            print(f"Quedan {repuesto.get_disponibles()} {repuesto.nombre}")
        else:
            print(f"el repuesto {nombre_repuesto} no esta disponible en este almacen")

    def adquirir_repuesto(self, nombre_repuesto: str, almacen: Almacen, n: int):
        """Adquiere una cantidad de repuestos restando stock del almacén si es válido."""
        try:
            if n <= 0:
                raise ValueError("La cantidad a adquirir debe ser mayor que cero")

            repuesto = almacen.buscar_repuesto(nombre_repuesto)
            if repuesto is None:
                raise LookupError(f"El repuesto '{nombre_repuesto}' no está disponible en el almacén")

            repuesto.retirar_stock(n)
            print(f"{self.usuario} ha adquirido {n} unidades de {nombre_repuesto}.")
        except Exception as e:
            print(f"Error al adquirir repuesto: {e}")

    def comparar_precios(self, nombre_repuesto: str, almacenes: list[Almacen]):
        """Busca el almacén con el menor precio para un repuesto dado y lo devuelve."""
        mejor_precio = None
        mejor_almacen = None

        for almacen in almacenes:
            repuesto = almacen.buscar_repuesto(nombre_repuesto)
            if repuesto is None:
                continue

            precio_unitario = repuesto.precio
            if mejor_precio is None or precio_unitario < mejor_precio:
                mejor_precio = precio_unitario
                mejor_almacen = almacen

        if mejor_almacen is None:
            print(f"No se encontró el repuesto '{nombre_repuesto}' en los almacenes proporcionados.")
            return None

        print(f"El mejor precio de '{nombre_repuesto}' es {mejor_precio} en {mejor_almacen.nombre}.")
        return mejor_almacen, mejor_precio


class Operario(Usuario):
    """Usuario que gestiona stock y catálogo en un almacén."""

    def __init__(self, usuario, almacen: Almacen):
        super().__init__(usuario)
        self.almacen = almacen

    def __str__(self):
        return f"Operario {self.usuario} (Almacén: {self.almacen.nombre})"

    def añadir_repuesto(self, repuesto: Repuesto):
        """Agrega un repuesto al almacén asociado."""
        self.almacen.agregar_catalogo(repuesto)

    def cambiar_stock(self, nombre_repuesto: str, n: int):
        """Ajusta stock de un repuesto, positivo para añadir, negativo para retirar."""
        try:
            repuesto = self.almacen.buscar_repuesto(nombre_repuesto)

            if repuesto is None:
                raise LookupError(f"El repuesto '{nombre_repuesto}' no existe en el almacén")

            if n > 0:
                repuesto.agregar_stock(n)
            else:
                repuesto.retirar_stock(-n)
        except Exception as e:
            print(f"Error al cambiar stock: {e}")


def main():
    try:
        print("=== Sistema de Mantenimiento de la Flota Espacial ===\n")

        # 1. Crear naves de diferentes tipos
        print("1. Creando naves:")
        estacion = Estacion_Espacial("Outpost 42", "EST-001", 1234, tripulacion=120, pasaje=0, ubicacion=Ubicacion.Endor)
        nave_estelar = Nave_Estelar("Executor", "NES-002", 5678, tripulacion=5000, pasaje=1000, clase=Clase.Ejecutor)
        caza = Caza_Estelar("TIE Fighter", "CZA-007", 9876, dotacion=1)
        print(f"- {estacion}")
        print(f"- {nave_estelar}")
        print(f"- {caza}\n")

        # 2. Crear almacenes con repuestos iniciales
        print("2. Creando almacenes con repuestos:")
        repuesto1 = Repuesto("Motor hiperespacial", "Initech", stock=5, precio=3000.0)
        repuesto2 = Repuesto("Panel de energia", "WayneTech", stock=10, precio=450.0)
        repuesto3 = Repuesto("Escudo deflector", "Stark", stock=3, precio=1200.0)
        repuesto4 = Repuesto("Motor hiperespacial", "CheapParts", stock=8, precio=2500.0)  # Mismo nombre, precio diferente

        almacen_central = Almacen("Almacén Central", "Sector 7", catalogo=[repuesto1, repuesto2])
        almacen_secundario = Almacen("Almacén Secundario", "Sector 8", catalogo=[repuesto3, repuesto4])
        print(f"- {almacen_central}")
        print(f"- {almacen_secundario}\n")

        # 3. Operaciones de operarios: añadir repuestos, cambiar stock
        print("3. Operaciones de operarios:")
        ope1 = Operario("Juan", almacen_central)
        ope2 = Operario("Ana", almacen_secundario)
        print(f"- {ope1}")
        print(f"- {ope2}")

        # Añadir repuesto nuevo
        ope1.añadir_repuesto(Repuesto("Hiperimpulsor", "Galactic", stock=2, precio=5000.0))
        print("  - Juan añade 'Hiperimpulsor' al almacén central")

        # Cambiar stock (agregar)
        ope2.cambiar_stock("Escudo deflector", 5)
        print("  - Ana aumenta stock de 'Escudo deflector' en 5 unidades")

        # Cambiar stock (retirar)
        ope1.cambiar_stock("Panel de energia", -3)
        print("  - Juan reduce stock de 'Panel de energia' en 3 unidades\n")

        # 4. Operaciones de comandantes: consultar, adquirir, comparar precios
        print("4. Operaciones de comandantes:")
        com1 = Comandante("Leia", estacion)
        com2 = Comandante("Han", nave_estelar)
        print(f"- {com1}")
        print(f"- {com2}")

        # Consultar disponibilidad
        print("  - Leia consulta disponibilidad de 'Motor hiperespacial':")
        com1.consultar_disponibilidad("Motor hiperespacial", almacen_central)

        # Adquirir repuesto
        print("  - Leia adquiere 2 unidades de 'Motor hiperespacial':")
        com1.adquirir_repuesto("Motor hiperespacial", almacen_central, 2)

        # Comparar precios entre almacenes
        print("  - Han compara precios de 'Motor hiperespacial' en ambos almacenes:")
        com2.comparar_precios("Motor hiperespacial", [almacen_central, almacen_secundario])

        # Usar métodos de utilidad en Repuesto
        print("\n5. Utilidades de repuestos:")
        motor = almacen_central.buscar_repuesto("Motor hiperespacial")
        if motor:
            print(f"  - Precio total de 3 motores: {motor.precio_total(3)} cr")
            print(f"  - ¿Disponible 10 unidades? {motor.es_disponible(10)}")
            print(f"  - Actualizando precio a 3200.0 cr")
            motor.actualizar_precio(3200.0)
            print(f"  - Nuevo precio: {motor.precio} cr")

        # 6. Utilidades de almacén: inventario, búsqueda por proveedor, eliminar
        print("\n6. Utilidades de almacenes:")
        print("  - Inventario del almacén central:")
        for nombre, stock in almacen_central.inventario().items():
            print(f"    {nombre}: {stock} unidades")

        print("  - Repuestos de 'WayneTech' en almacén central:")
        for rep in almacen_central.buscar_por_proveedor("WayneTech"):
            print(f"    {rep}")

        print("  - Eliminando 'Panel de energia' del almacén central:")
        eliminado = almacen_central.eliminar_repuesto("Panel de energia")
        print(f"    Eliminado: {eliminado}")

        # 7. Mostrar catálogos finales
        print("\n7. Catálogos finales:")
        print("  - Almacén Central:")
        almacen_central.mostrar_catalogo()
        print("  - Almacén Secundario:")
        almacen_secundario.mostrar_catalogo()

        # 8. Forzar errores para probar excepciones
        print("\n8. Pruebas de excepciones:")
        try:
            com1.adquirir_repuesto("Panel de energia", almacen_central, -1)  # Cantidad inválida
        except Exception as e:
            print(f"  - Error esperado en adquisición: {e}")

        try:
            ope1.cambiar_stock("NoExiste", 1)  # Repuesto no existe
        except Exception as e:
            print(f"  - Error esperado en cambio de stock: {e}")

    except Exception as e:
        print(f"Ocurrió un error en la ejecución principal: {e}")


if __name__ == "__main__":
    main()
        