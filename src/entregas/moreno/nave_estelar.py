from numeracion import ClaseNave

class Nave_Estelar:

    def __init__(self, tripulacion: int, pasaje: int, clase: ClaseNave):
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__clase = clase

    def mostrar_info(self):
        print(self)

    def capacidad_total(self) -> int:
        #total de personas en la nave.
        return self.__tripulacion + self.__pasaje

    def cambiar_clase(self, nueva_clase: ClaseNave):
        #poder cambiar la clase de la nave.
        self.__clase = nueva_clase

    def __str__(self):
        return f"Nave Estelar | Tripulación: {self.__tripulacion} | Pasaje: {self.__pasaje} | Clase: {self.__clase.value}"