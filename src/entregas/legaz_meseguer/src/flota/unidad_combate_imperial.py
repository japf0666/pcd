from utils.enumeraciones import Ubicacion, ClaseNaveEstelar
from abc import ABC

"""
Clase Unidad Combate Imperial
"""




class UnidadCombateImperial(ABC):
    
    def __init__(self, id_combate : str , clave_transmision : int):
        
        self.id_combate = id_combate
        self.clave_transmision = clave_transmision
        
        
class Nave(UnidadCombateImperial):
    
    def __init__(self, id_combate : str, clave_transmision : int, nombre : str):
        
        super().__init__(id_combate, clave_transmision)
        self.nombre = nombre
        self.catalogo_repuestos = []
        
    
    
class EstacionEspacial(Nave):
    
    def __init__(self, id_combate : str, clave_transmision : int, nombre : str, tripulacion : int, pasaje : int, ubicacion : Ubicacion):
        super().__init__(id_combate, clave_transmision, nombre)
        
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion
        
        
        
class NaveEstelar(Nave):
    
    def __init__(self, id_combate : str, clave_transmision : int, nombre : str, tripulacion : int, pasaje : int, clase : ClaseNaveEstelar):
        
        super().__init__(id_combate, clave_transmision, nombre)
        
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase


class CazaEstelar(Nave):
    
    def __init__(self, id_combate : str, clave_transmision : int, nombre : str, dotacion):
    
      super().__init__(id_combate, clave_transmision, nombre)
      
      self.dotacion = dotacion

        