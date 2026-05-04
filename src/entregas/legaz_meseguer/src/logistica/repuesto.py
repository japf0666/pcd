

class Repuesto:
    
    def __init__(self, nombre : str, proveedor : str, cantidad : int, precio : float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio
        
    def get_cantidad(self):
        
        return self.__cantidad
    
    def set_cantidad(self, valor):
        
        if valor > 0:
            self.__cantidad = valor
        else:
            raise ValueError('Cantidad no puede ser negativa')