from abc import ABC, abstractmethod
from enum import Enum
from typing import List

# ==================== EXCEPCIONES ====================

class ErrorStockInsuficiente(Exception):
    pass

class ErrorRepuestoNoEncontrado(Exception):
    pass

class ErrorUbicacionInvalida(Exception):
    pass

class ErrorClaseNaveInvalida(Exception):
    pass

# ==================== ENUMERACIONES ====================

class ClaseNave(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

class Ubicacion(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

# ==================== CLASES ABSTRACTAS ====================

class UnidadCombate(ABC): # Clase abstracta de base para naves y estaciones
    # Que guardan atributos privados como el id_combate y la clave cifrada, y métodos para acceder a ellos
    def __init__(self, id_combate: str, clave_cifrada: int):
        self._id_combate = id_combate
        self._clave_cifrada = clave_cifrada

    def get_id(self) -> str: # Método para obtener el id de combate
        return self._id_combate

    def get_clave_cifrada(self) -> int: # Método para obtener la clave cifrada
        return self._clave_cifrada

    @abstractmethod
    def mostrar_info(self) -> str: # Método abstracto para mostrar la información de la unidad de combate, que debe ser implementado por las clases hijas
        pass

class Nave(UnidadCombate, ABC): # Clase abstracta de base que herede de la clase UnidadCombate, y que tenga atributos privados como el nombre y el catálogo de repuestos, y métodos para acceder a ellos
    # Además, debe tener un método para añadir repuestos al catálogo, y otro para consultar el catálogo de repuestos
    # Y este es la clase base para las clases NaveEstelar, CazaEstelar y EstacionEspacial
    def __init__(self, nombre: str, catalogo_repuesto: List[str], id_combate: str, clave_cifrada: int):
        super().__init__(id_combate, clave_cifrada) # Llamamos al constructor de la clase padre para inicializar el id_combate y la clave_cifrada
        self._nombre = nombre
        self._catalogo_repuesto = catalogo_repuesto

    def get_nombre(self) -> str: # Método para obtener el nombre de la nave
        return self._nombre

    def añadir_repuesto(self, repuesto: str): # Método para añadir un repuesto al catálogo de repuestos, evitando duplicados
        if repuesto not in self._catalogo_repuesto: # Hemos supuesto de que no habrá una pieza que se llame igual pero sea diferente,
            # por lo que el nombre del repuesto es su identificador único
            self._catalogo_repuesto.append(repuesto)

    def consultar_repuesto(self) -> List[str]: # Método para consultar el catálogo de repuestos, devolviendo una copia de la lista para evitar modificaciones externas
        return self._catalogo_repuesto.copy()

    @abstractmethod # Método abstracto para mostrar la información de la nave, que debe ser implementado por sus clases hijas
    def mostrar_info(self) -> str:
        pass

# ==================== NAVES ====================

class NaveEstelar(Nave): # Clase que hereda de Nave, y que tiene atributos privados como la tripulación, el pasaje y la clase de nave, y métodos para acceder a ellos
    def __init__(self, nombre: str, catalogo_repuesto: List[str], id_combate: str, clave_cifrada: int,
                 tripulacion: int, pasaje: int, clase: ClaseNave):
        super().__init__(nombre, catalogo_repuesto, id_combate, clave_cifrada)
        self._tripulacion = tripulacion
        self._pasaje = pasaje
        if not isinstance(clase, ClaseNave): # Comprobamos que la clase de nave es válida, es decir, 
            # que es una instancia de la enumeración ClaseNave, y si no lo es, lanzamos una excepción
            raise ErrorClaseNaveInvalida
        self._clase = clase

    def get_tripulacion_nav_estelar(self): # Método para obtener la tripulación de la nave estelar
        return self._tripulacion

    def get_pasaje_nav_estelar(self): # Método para obtener el pasaje de la nave estelar
        return self._pasaje

    def get_clase(self): # Método para obtener la clase de la nave estelar, devolviendo el valor de la enumeración para que sea más legible
        return self._clase.value 

    def mostrar_info(self): # Método para mostrar la información de la nave estelar, que incluye el nombre y el id de combate
        return f"Nave Estelar: {self._nombre}\nID Combate: {self.get_id()}"

    def __str__(self): # Método para representar la nave estelar como una cadena, que simplemente devuelve la información de la nave
        return self.mostrar_info()

class CazaEstelar(Nave): # Clase que hereda de Nave, y que tiene un atributo privado como la dotación, y un método para acceder a ella
    def __init__(self, nombre: str, catalogo_repuesto: List[str], id_combate: str, clave_cifrada: int, dotacion: int):
        super().__init__(nombre, catalogo_repuesto, id_combate, clave_cifrada)
        self._dotacion = dotacion

    def get_dotacion(self): # Método para obtener la dotación del caza estelar
        return self._dotacion

    def mostrar_info(self): # Método para mostrar la información del caza estelar, que incluye el nombre
        return f"Caza Estelar: {self._nombre}"

    def __str__(self): # Método para representar el caza estelar como una cadena, que simplemente devuelve la información del caza
        return self.mostrar_info()

class EstacionEspacial(Nave): # Clase que hereda de Nave, y que tiene atributos privados como la tripulación, el pasaje y la ubicación, y métodos para acceder a ellos
    def __init__(self, nombre: str, catalogo_repuesto: List[str], id_combate: str, clave_cifrada: int,
                 tripulacion: int, pasaje: int, ubicacion: Ubicacion):
        super().__init__(nombre, catalogo_repuesto, id_combate, clave_cifrada)
        self._tripulacion = tripulacion
        self._pasaje = pasaje
        if not isinstance(ubicacion, Ubicacion): # Comprobamos que la ubicación es válida, es decir, que es una instancia de la enumeración Ubicacion, y si no lo es, lanzamos una excepción
            raise ErrorUbicacionInvalida
        self._ubicacion = ubicacion 

    def get_ubicacion(self): # Método para obtener la ubicación de la estación espacial, devolviendo el valor de la enumeración para que sea más legible
        return self._ubicacion.value # .value para devolver el valor de la enumeración en lugar del objeto de la enumeración

    def mostrar_info(self): # Método para mostrar la información de la estación espacial, que incluye el nombre
        return f"Estación Espacial: {self._nombre}" 

    def __str__(self):
        return self.mostrar_info()

# ==================== REPUESTOS ====================

class Repuesto: # Clase que representa un repuesto, con atributos privados como el nombre, la cantidad y el precio, y métodos para acceder a ellos    
    def __init__(self, nombre: str, cantidad: int, precio: float):
        self._nombre = nombre
        self.__cantidad = cantidad
        self._precio = precio

    def get_nombre(self): # Método para obtener el nombre del repuesto
        return self._nombre

    def get_cantidad(self): # Método para obtener la cantidad del repuesto
        return self.__cantidad

    def set_cantidad(self, cantidad): # Método para establecer la cantidad del repuesto, que solo puede ser modificada a través de este método para controlar las modificaciones y evitar cantidades negativas
        if cantidad < 0:
            raise ValueError
        self.__cantidad = cantidad

    def get_precio(self): # Método para obtener el precio del repuesto
        return self._precio

    def añadir_stock(self, cantidad): # Método para añadir stock al repuesto, que solo puede ser modificado a través de este método para controlar las modificaciones y evitar cantidades negativas
        if cantidad < 0:
            raise ValueError
        self.__cantidad += cantidad

    def retirar_stock(self, cantidad): # Método para retirar stock del repuesto, que solo puede ser modificado a través de este método para controlar las modificaciones y evitar cantidades negativas
        if cantidad <= 0:
            raise ValueError
        if cantidad <= self.__cantidad:
            self.__cantidad -= cantidad
            return cantidad
        retirado = self.__cantidad
        self.__cantidad = 0
        return retirado

    def __str__(self): # Método para representar el repuesto como una cadena
        return f"Repuesto: {self._nombre}, Cantidad: {self.__cantidad}, Precio: {self._precio}€"

    def __eq__(self, other): # Método para comparar dos repuestos, devolviendo True si son iguales y False en caso contrario
        return isinstance(other, Repuesto) and self._nombre == other._nombre

# ==================== ALMACEN ====================

class Almacen: # Clase que representa un almacén, con atributos privados como el nombre, la ubicación y el catálogo de repuestos, y métodos para acceder a ellos
    def __init__(self, nombre, ubicacion):
        self._nombre = nombre
        self._ubicacion = ubicacion
        self._catalogo = []

    def get_nombre(self): # Método para obtener el nombre del almacén
        return self._nombre

    def get_ubicacion(self): # Método para obtener la ubicación del almacén
        return self._ubicacion

    def añadir_repuesto(self, repuesto): # Método para añadir un repuesto al catálogo del almacén, evitando duplicados
        for rep in self._catalogo:
            if rep.get_nombre() == repuesto.get_nombre(): # Hemos supuesto de que no habrá una pieza que se llame igual pero sea diferente, por lo que el nombre del repuesto es su identificador único 
                raise ValueError("El repuesto ya existe en el catálogo")
        self._catalogo.append(repuesto)

    def eliminar_repuesto(self, nombre): # Método para eliminar un repuesto del catálogo del almacén, buscando el repuesto por su nombre, y si no se encuentra, lanzando una excepción
        for rep in self._catalogo:
            if rep.get_nombre() == nombre:
                return self._catalogo.remove(rep)
        raise ErrorRepuestoNoEncontrado

    def consultar_stock(self, nombre): # Método para consultar el stock de un repuesto en el catálogo del almacén, buscando el repuesto por su nombre, y si no se encuentra, devolviendo 0
        for rep in self._catalogo:
            if rep.get_nombre() == nombre:
                return rep.get_cantidad()
        return 0

    def actualizar_stock(self, nombre, cantidad): # Método para actualizar el stock de un repuesto en el catálogo del almacén, buscando el repuesto por su nombre, y si no se encuentra, lanzando una excepción, y si la cantidad a retirar es mayor que el stock disponible, lanzando una excepción de stock insuficiente
        for rep in self._catalogo:
            if rep.get_nombre() == nombre:
                if cantidad > rep.get_cantidad():
                    raise ErrorStockInsuficiente
                rep.set_cantidad(rep.get_cantidad() - cantidad)
                return
        raise ErrorRepuestoNoEncontrado

    def valor_total_stock(self): # Método para calcular el valor total del stock del almacén, sumando el producto de la cantidad y el precio de cada repuesto en el catálogo
        return sum(r.get_cantidad() * r.get_precio() for r in self._catalogo)

    def __str__(self): # Método para representar el almacén como una cadena, que incluye el nombre, la ubicación y el número de repuestos disponibles, y la información de cada repuesto
        info = f"Almacén: {self._nombre} ({self._ubicacion})\n"
        info += f"Repuestos disponibles: {len(self._catalogo)}\n"
        for repuesto in self._catalogo:
            info += f"  - {repuesto}\n"
        return info
    

#-----------------------------------------------------------------------------
# Cçodigo para comprobar las instacias de las clases y probar funcionalidades
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    print("SISTEMA DE MANTENIMIENTO - FLOTA IMPERIAL")
    print("CREACIÓN DE ALMACÉN")
    almacen = Almacen("Almacén Central", "Coruscant")
    
    rep1 = Repuesto("Motor Hiperespacial",  10, 50000.0)
    rep2 = Repuesto("Escudos Deflectores",  25, 15000.0)
    rep3 = Repuesto("Panel Solar",  100, 500.0)
    
    almacen.añadir_repuesto(rep1)
    almacen.añadir_repuesto(rep2)
    almacen.añadir_repuesto(rep3)
    
    print(almacen)
    print(f"Valor total del stock: {almacen.valor_total_stock()}€\n")
    
    # Crear naves
    print("==============================================================")
    print("CREACIÓN DE NAVES")
    print("==============================================================")
    
# Crear naves
    nave1 = NaveEstelar("Executor", ["Motor Hiperespacial", "Escudos Deflectores"],
                    "DS-001", 7734, 280000, 5000, ClaseNave.EJECUTOR)
    print(nave1)
    print()
    
    nave2 = CazaEstelar("TIE Fighter", ["Panel Solar", "Propulsor"],
                       "TF-042", 1138, 1)
    print(nave2)
    print()
    
    nave3 = EstacionEspacial("Estación Endor", ["Generador de Energía", "Sistema Soporte Vital"],
                            "ES-007", 9999, 5000, 1000, Ubicacion.ENDOR)
    print(nave3)
    print()
    
    # Probar funcionalidades
    print("==============================================================")
    print("PRUEBA DE FUNCIONALIDADES")
    print("==============================================================")
    
    print(f"Repuestos antes: {nave1.consultar_repuesto()}")
    nave1.añadir_repuesto("Blaster Pesado")
    print(f"Repuestos después: {nave1.consultar_repuesto()}\n")
    
    stock = almacen.consultar_stock("Panel Solar")
    print(f"Stock de Paneles Solares: {stock}")
    
    almacen.actualizar_stock("Panel Solar", 10)
    nuevo_stock = almacen.consultar_stock("Panel Solar")
    print(f"Stock después de retirar 10: {nuevo_stock}\n")
    
    # Probar excepciones
    print("==============================================================")
    print("PRUEBA DE EXCEPCIONES")
    print("==============================================================")
    
    try:
        almacen.actualizar_stock("Motor Hiperespacial", 100)
    except ErrorStockInsuficiente as e:
        print(f"Excepción capturada {e}")
    
    try:
        almacen.eliminar_repuesto("Repuesto Fantasma")
    except ErrorRepuestoNoEncontrado as e:
        print(f"Excepción capturada {e}")

