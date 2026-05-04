from abc import ABC, abstractmethod

class UnidadCombate(ABC):

    def __init__(self, id_combate: str, clave_cifrada: int):
        self.__id_combate = id_combate
        self.__clave_cifrada = clave_cifrada

    def get_id_combate(self) -> str:
        return self.__id_combate

    def get_clave_cifrada(self) -> int:
        return self.__clave_cifrada

    def transmitir_mensaje(self, mensaje: str):
        #Simula una transmisión cifrada
        print(f"[Unidad {self.__id_combate}] Transmitiendo mensaje cifrado: {mensaje}")

    @abstractmethod
    def mostrar_info(self):
        #Cada unidad debe implementar su propia forma de mostrar información
        pass

    def __str__(self):
        return f"Unidad de Combate | ID: {self.__id_combate}"