
class Repuesto:
    def __init__(self, nombre: str, proveedor: str, cantidad: int,precio: float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio

    def get_cantidad(self) -> int:
        #Devolver la cantidad actual en stock de este repuesto.
        return self.__cantidad

    def añadir_stock(self, cantidad: int):
        #Añadir una cantidad al stock de este repuesto3
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        self.__cantidad += cantidad

    def retirar_stock(self, cantidad: int):
        #Retirar una cantidad del stock de este repuesto
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

        if cantidad > self.__cantidad:
            raise ValueError("No hay suficiente stock disponible")

        self.__cantidad -= cantidad

    def calcular_valor_total(self) -> float:
        #Calcular el valor total del stock de este repuesto
        return self.__cantidad * self.precio

    
    def __str__(self):
        return f"{self.nombre} ({self.proveedor}) - Stock: {self.__cantidad} - Precio: {self.precio}€"