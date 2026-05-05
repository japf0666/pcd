from naves import Nave
from almacen_piezas import Almacen


class MiImperio():
    def __init__(self):
        self.naves = set() # conjunto de Nave
        self.almacenes = set() # conjunto de Almacen

    def añadir_nave(self, nave:Nave):
        if not isinstance(nave, Nave):
            raise ValueError("La nave debe ser una instancia de Nave")
        self.naves.add(nave)
    
    def añadir_almacen(self, almacen:Almacen):
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        self.almacenes.add(almacen)
    
    # Iteradores para mostrar naves y almacenes
    def mostrar_naves(self):
        for nave in self.naves:
            yield nave

    def mostrar_almacenes(self):
        for almacen in self.almacenes:
            yield almacen
            