from typing import List
from repuesto import Repuesto

class Nave:
    def __init__(self, nombre: str, catalogo_repuestos: List[Repuesto]):
        self.nombre = nombre
        self.catalogo_repuestos = catalogo_repuestos

    def mostrarInfo(self):
        print(self)

    def consular_repuesto(self, nombre: str) -> Repuesto: #en diagrama de clases devolvia bool, pero en practica es mejor retornar Repuesto
        for repuesto in self.catalogo_repuestos:
            if repuesto.nombre == nombre:
                return repuesto
        return None


    def adquirir_repuesto(self, nombre: str, cantidad: int): #se agrega el parametro de cantidad
        repuesto = self.consular_repuesto(nombre)
        if repuesto:
            repuesto.añadir_stock(cantidad)
        else:
            raise ValueError("Repuesto no encontrado en el catálogo de la nave")