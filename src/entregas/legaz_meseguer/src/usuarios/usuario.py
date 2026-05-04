from abc import ABC
from src.logistica.repuesto import Repuesto
from src.logistica.almacen import Almacen


class Usuario(ABC):

    def __init__(self, nombre: str, id_usuario: str):
        self.nombre = nombre
        self.id_usuario = id_usuario


class Comandante(Usuario):

    def consultar_repuesto(self, nombre_pieza: str, almacen: Almacen):
        print(f"Comandante : {self.nombre} consultando en Almacén {almacen.nombre}")
        for repuesto in almacen.inventario:
            if repuesto.nombre == nombre_pieza:
                print(
                    f"Pieza encontrada : {repuesto.nombre} | Stock: {repuesto.get_cantidad()} | Precio: {repuesto.precio} créditos"
                )
                return repuesto

        print(f"La pieza {nombre_pieza} no esta disponible en este almacen ")
        return None

    def adquirir_repuesto(self, nombre_pieza: str, almacen: Almacen):
        repuesto = self.consultar_repuesto(nombre_pieza, almacen)
        if repuesto and repuesto.get_cantidad() > 0:
            nuevo_stock = repuesto.get_cantidad() - 1
            repuesto.set_cantidad(nuevo_stock)
            print(f"La pieza {nombre_pieza} ha sido comprada con exito ")

        elif repuesto:
            print("No hay stock")


class Opeario(Usuario):

    def registrar_repuesto(self, repuesto: Repuesto, almacen: Almacen):
        almacen.inventario.append(repuesto)
        print(
            f"Se ha registrado la pieza {repuesto.nombre} en el almacen {almacen.nombre}"
        )

    def actualizar_stock(self, repuesto: Repuesto, cantidad: int):
        repuesto.set_cantidad(cantidad)
        print(
            f"Operario {self.nombre} ha actualizado el stock de {repuesto.nombre} a {cantidad}"
        )
