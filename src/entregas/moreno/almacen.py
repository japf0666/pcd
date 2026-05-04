from typing import List
from repuesto import Repuesto

class Almacen:
    
   #Clase que representa la abstraccion de un almacén de repuestos.
    

    def __init__(self, nombre: str, ubicacion: str):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.catalogo: List[Repuesto] = []

    def añadir_repuesto(self, repuesto: Repuesto):
        
        #Añadimos un repuesto al catálogo del almacén, osea a la lista.
        
        for r in self.catalogo:
            if r.nombre == repuesto.nombre:
                raise ValueError("El repuesto ya existe en el catálogo") # Si el repuesto ya existe, no lo añadimos
                                                                        #gestión de excepciones y lanzamos un error

        self.catalogo.append(repuesto)

    def eliminar_repuesto(self, nombre: str):
        
        """ Eliminar un repuesto del catálogo."""
        
        for repuesto in self.catalogo:
            if repuesto.nombre == nombre:
                self.catalogo.remove(repuesto)
                return

        raise ValueError("El repuesto no existe en el catálogo")

    def buscar_repuesto(self, nombre: str) -> Repuesto:
        #Buscar un repuesto por su nombre.
        for repuesto in self.catalogo:
            if repuesto.nombre == nombre:
                return repuesto

        raise ValueError("Repuesto no encontrado")

    def actualizar_stock(self, nombre: str, cantidad: int):
        
        #Actualizar el stock de un repuesto.
        
        repuesto = self.buscar_repuesto(nombre)
        if cantidad > 0:
            repuesto.añadir_stock(cantidad)
        else:
            repuesto.retirar_stock(abs(cantidad))

    def mostrar_catalogo(self):
        
        #Muestra todos los repuestos disponibles.
        
        print(f"\n Catálogo del almacén: {self.nombre}\n")

        if not self.catalogo:
            print("No hay repuestos disponibles")
            return

        for repuesto in self.catalogo:
            print(repuesto)

    def calcular_valor_total_inventario(self) -> float:
        
        #Calcula el valor total de todos los repuestos del almacén.
        
        total = 0

        for repuesto in self.catalogo:
            total += repuesto.calcular_valor_total()

        return total

