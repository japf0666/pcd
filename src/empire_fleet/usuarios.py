from excepciones import DatoInvalidoError, RepuestoNoAutorizadoError
from interfaces import IServiciosCompras, Nave


class Comandante:
    """
    El comandante trabaja sobre la interfaz de servicios de compras.
    """

    def __init__(self, nombre: str, nave: Nave) -> None:
        if not nombre or not isinstance(nombre, str):
            raise DatoInvalidoError("El nombre del comandante debe ser un texto no vacío.")
        if not isinstance(nave, Nave):
            raise DatoInvalidoError("El comandante debe estar asociado a una nave.")

        self.nombre: str = nombre
        self.nave: Nave = nave
        nave.asignar_comandante(self)

    '''
    def consultar_repuestos_disponibles(self, almacen: Almacen) -> list[Repuesto]:
        disponibles: list[Repuesto] = []
        for repuesto in almacen.consultar_repuestos(self):
            if self.nave.admite_repuesto(repuesto.nombre):
                disponibles.append(repuesto)
        return disponibles

    def solicitar_repuesto(self, almacen: Almacen, nombre_repuesto: str, cantidad: int) -> str:
        if not self.nave.admite_repuesto(nombre_repuesto):
            raise RepuestoNoAutorizadoError(
                f"La nave '{self.nave.nombre}' no admite el repuesto '{nombre_repuesto}'."
            )

        coste = almacen.proveer_repuesto(self, nombre_repuesto, cantidad)
        return (
            f"Comandante '{self.nombre}': compra realizada -> "
            f"{cantidad} unidad(es) de '{nombre_repuesto}' para '{self.nave.nombre}'. "
            f"Coste total: {coste:.2f} créditos."
        )

    def __str__(self) -> str:
        return f"Comandante(nombre='{self.nombre}', nave='{self.nave.nombre}')"
'''

class OperarioAlmacen:
    """
    El operario trabaja sobre la interfaz de gestión de inventario.
    """

    def __init__(self, nombre: str) -> None:
        if not nombre or not isinstance(nombre, str):
            raise DatoInvalidoError("El nombre del operario debe ser un texto no vacío.")
        self.nombre: str = nombre

'''
    def registrar_repuesto(self, almacen: Almacen, repuesto: Repuesto) -> None:
        almacen.alta_repuesto(self, repuesto)

    def reponer(self, almacen: Almacen, nombre_repuesto: str, cantidad: int) -> None:
        almacen.reponer_stock(self, nombre_repuesto, cantidad)

    def retirar_catalogo(self, almacen: Almacen, nombre_repuesto: str) -> None:
        almacen.eliminar_repuesto(self, nombre_repuesto)

    def __str__(self) -> str:
        return f"OperarioAlmacen(nombre='{self.nombre}')"
        '''