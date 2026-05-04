from numeracion import Ubicacion

class Estacion_espacial:
    def __init__(self, tripulacion: int, pasaje: int, ubicacion: Ubicacion):
        self.__tripulacion= tripulacion
        self.__pasaje= pasaje
        self.__ubicacion= ubicacion
    
    def mostrar_info(self):
        print(self)
        
    def mover_estacion(self, NuevaUbicacion: Ubicacion):
        self.__ubicacion = NuevaUbicacion
    
    def __str__(self):
        return f"{self.__tripulacion} -> {self.__pasaje} --> {self.__ubicacion}"
