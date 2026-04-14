from abc import ABC, abstractmethod
from enumeraciones import ClaseNaveEstelar, UbicacionEstacion

class UnidadCombateImperial(ABC):
    """
    Clase abstracta que representa una unidad de combate imperial en la empresa 
    Imperio Galactico (Representa naves, vehiculos terrestres y demás vehiculos).
    """
    # contador para la clave
    _ultima_clave = 0

    def __init__(self, id_combate:str):
        if not isinstance(id_combate, str) or not id_combate.strip():
            raise ValueError("El id_combate debe ser una cadena de texto no vacía.")
        
        UnidadCombateImperial._ultima_clave += 1
        self.id_combate = id_combate
        self.clave = UnidadCombateImperial._ultima_clave

    def transmitir_mensaje(self, mensaje:str):
        return f"""Unidad de combate imperial {self.id_combate} transmite: 
                {mensaje} con clave {self.clave}"""

    @abstractmethod
    # Todos los vehiculos tiene que implementar el metodo __str__ para mostrar su información
    def __str__(self):
        pass

class Nave(UnidadCombateImperial, ABC):
    """
    Clase abstracta que representa una nave en la empresa Imperio Galactico.
    """
    def __init__(self, nombre:str, piezas:list):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacío")
        if not isinstance(piezas, list) or not piezas:
            raise ValueError("Las piezas deben ser una lista no vacía")
        
        super().__init__(nombre)

        self.nombre = nombre
        self.piezas = piezas
        self.comandante = None # Lo asignamos luego al crear al comandante

    def consultar_piezas(self):
        return f"Nave {self.nombre} tiene las siguientes piezas: {', '.join(self.piezas)}"
    
    def repuesto_valido(self, repuesto:str):
        return repuesto in self.piezas
    
    def _asignar_comandante(self, comandante):
        self.comandante = comandante

    @abstractmethod
    # clases hijas deben implementar el metodo atacar
    def atacar(self):
        pass

class EstacionEspacial(Nave):
    def __init__(self, nombre:str, repuestos:list, tripulacion:int, 
                 pasaje:int, ubicacion:UbicacionEstacion):

        if not isinstance(tripulacion, int) or tripulacion < 0:
            raise ValueError("La tripulación debe ser un número entero no negativo")
        if not isinstance(pasaje, int) or pasaje < 0:
            raise ValueError("El pasaje debe ser un número entero no negativo")
        if not isinstance(ubicacion, UbicacionEstacion):
            raise ValueError("La ubicación debe ser una instancia de UbicacionEstacion")
        super().__init__(nombre, repuestos)

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def atacar(self):
        return f"""Estación espacial ({self.nombre}) ataca desde {self.ubicacion.value}
                    con un disparador láser"""
    
    def __str__(self):
        return f"""Estación espacial ({self.nombre}) ubicada en {self.ubicacion.value} 
                con tripulación de {self.tripulacion} y pasaje de {self.pasaje}"""
    
class NaveEstelar(Nave):
    def __init__(self, nombre:str, repuestos:list, tripulacion:int, 
                 pasaje:int, clase:ClaseNaveEstelar):
        # Hereda de la clase Nave, y esta a su vez hereda de la clase UnidadCombateImperial, 
        # por lo que llamando al init de la clase Nave se llama al init de la clase UnidadCombateImperial
        if not isinstance(tripulacion, int) or tripulacion < 0:
            raise ValueError("La tripulación debe ser un número entero no negativo")
        if not isinstance(pasaje, int) or pasaje < 0:
            raise ValueError("El pasaje debe ser un número entero no negativo")
        if not isinstance(clase, ClaseNaveEstelar):
            raise ValueError("La clase debe ser una instancia de ClaseNaveEstelar")
        
        super().__init__(nombre, repuestos)

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def atacar(self):
        return f"""Nave estelar ({self.nombre}) de clase {self.clase.value} ataca con misiles"""

    def __str__(self):
        return f"""Nave estelar ({self.nombre}) de clase {self.clase.value} 
                con tripulación de {self.tripulacion} y pasaje de {self.pasaje}"""

class CazaEstelar(Nave):
    def __init__(self, nombre:str, repuestos:list, dotacion:int):

        if not isinstance(dotacion, int) or dotacion < 0:
            raise ValueError("La dotación debe ser un número entero no negativo")
        
        super().__init__(nombre, repuestos)

        self.dotacion = dotacion
    
    def atacar(self):
        return f"""Caza estelar ({self.nombre}) ataca con cañones de iones"""
    
    def __str__(self):
        return f"""Caza estelar ({self.nombre}) con dotación de {self.dotacion}"""