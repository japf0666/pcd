# importamos los paquetes nevesarios para la implementación de la flota espacial
from abc import ABC, abstractmethod
from enum import Enum

#creamos una excepción personalizada para manejar el caso de stock insuficiente
class StockInsuficienteError(Exception):
    """Excepción lanzada cuando la cantidad pedida supera el stock disponible."""
    pass

# creamos la clase ubicacion como una enumeración para representar los diferentes lugares donde pueden estar las estaciones espaciales
class Ubicacion(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

# hacemos lo mismo para los diferentes tipos de mnaves
class ClaseNave(Enum):
    EJCUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

# definimos la clase abstracta Nave, que servirá como base para las clases EstacionEspacial y CazaEstelar
class UnidadCombate:
    def __init__(self, id_combate: str, clave_transmision: int): #añadimos los atributos id_combate y clave_transmision a la clase UnidadCombate
        self.id_combate = id_combate
        self.clave_transmision = clave_transmision

# la clase Nave es una clase abstracta que define la estructura básica de una nave espacial, con un método abstracto mostrar_info que 
# debe ser implementado por las clases hijas
class Nave(ABC):
    def __init__(self, nombre:str, catalogo_repuestos: list): #añadimos los atributos nombre y catalogo_repuestos a la clase Nave
        self.nombre = nombre
        self.catalogo_repuestos = catalogo_repuestos

    @abstractmethod # decorador que indica que el método mostrar_info es abstracto y debe ser implementado por las clases hijas
    def mostrar_info(self):
        pass

class EstacionEspacial(Nave): # la clase EstacionEspacial hereda de Nave y tiene atributos adicionales como tripulación, pasaje y lugar
    def __init__(self, nombre:str, catalogo: list, tripulacion: int, pasaje: int, lugar: Ubicacion):
        super().__init__(nombre, catalogo)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.lugar = lugar

    def mostrar_info(self): # implementamos el método mostrar_info para la clase EstacionEspacial, que imprime en pantalla los atributos de la estación espacial
        print(f"Nombre: {self.nombre}")
        print(f"Ubicación: {self.lugar.value}")

class CazaEstelar(Nave, UnidadCombate): # la clase CazaEstelar hereda de Nave y UnidadCombate, y tiene un atributo adicional dotación
    def __init__(self, nombre:str, catalogo: list, dotacion: int, id_combate: str, clave: int):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)
        self.dotacion = dotacion

    def mostrar_info(self): # implementamos el método mostrar_info para la clase CazaEstelar, que imprime en pantalla los atributos del caza estelar
        print(f"Nombre: {self.nombre}")
        print(f"ID Combate: {self.id_combate}")
        print(f"Dotación: {self.dotacion}")

class NaveEstelar(Nave, UnidadCombate): # la clase NaveEstelar hereda de Nave y UnidadCombate, y tiene atributos adicionales como tripulación, pasaje y tipo
    def __init__(self, nombre: str, catalogo: list, tripulacion: int, pasaje: int, tipo: ClaseNave, id_combate: str, clave: int):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.tipo = tipo

    def mostrar_info(self): # implementamos el método mostrar_info para la clase NaveEstelar, que imprime en pantalla los atributos de la nave estelar
        print(f"Nave Estelar: {self.nombre} | Clase: {self.tipo.value} | ID: {self.id_combate}")

class Repuesto: # la clase Repuesto representa una pieza de repuesto para las naves espaciales, con atributos como nombre, proveedor, cantidad y precio
    def __init__(self, nombre:str, proveedor:str, cantidad:int, precio:float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio
    
    @property # decorador que convierte el método cantidad en una propiedad, lo que permite acceder a ella como si fuera un atributo
    def cantidad(self):
        return self.__cantidad

    def extraer_repuesto(self, unidades:int): # método para extraer una cantidad de repuestos, que verifica si hay suficiente stock antes de realizar la extracción
        if unidades > self.__cantidad: 
            raise StockInsuficienteError(f"Stock insuficiente para el repuesto {self.nombre}. Cantidad disponible: {self.__cantidad}")
        self.__cantidad -= unidades
        return True
    
class Almacen: # la clase Almacen representa un lugar donde se almacenan los repuestos, con atributos como nombre, localización y un catálogo de piezas
    def __init__(self, nombre: str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo_piezas = [] # Lista de objetos Repuesto

    def anadir_repuesto(self, repuesto: Repuesto): # método para añadir un repuesto al catálogo de piezas del almacén
        self.catalogo_piezas.append(repuesto)

# codigo de prueba
if __name__ == "__main__":
    print("--- INICIANDO SISTEMA MILIMPERIO ---")
    
    # Instanciación correcta
    caza = CazaEstelar("TIE Fighter", ["Motor Iónico", "Láser"], 1, "TIE-001", 12345)
    estacion = EstacionEspacial("Estrella de la Muerte", ["Panel", "Reactor"], 342953, 843342, Ubicacion.ENDOR)
    motor = Repuesto("Motor Iónico", "Sienar", 5, 2500.50)
    
    # Impresión en pantalla
    caza.mostrar_info()
    estacion.mostrar_info()
    
    print("\n--- PRUEBA DE ADQUISICIÓN DE REPUESTOS ---")
    try:
        print("Intentando extraer 3 motores...")
        motor.extraer_repuesto(3)
        print(f"Éxito. Stock restante: {motor.cantidad}")
        
        print("Intentando extraer 10 motores...")
        motor.extraer_repuesto(10) # Esto desencadena el error
    except StockInsuficienteError as e:
        # Capturamos y tratamos la excepción
        print(f"EXCEPCIÓN CAPTURADA: {e}")

       