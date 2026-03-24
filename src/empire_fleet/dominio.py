from enumeraciones import UbicacionEstacion, ClaseNaveEstelar
from excepciones import (
    DatoInvalidoError,
    RepuestoNoAutorizadoError,
    StockInsuficienteError,
    RepuestoNoEncontradoError,
    UsuarioNoAutorizadoError
)
from interfaces import Nave, UnidadCombate, IGestionInventario, IServiciosCompras
from usuarios import Comandante, OperarioAlmacen

class Repuesto:
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: float) -> None:
        if not nombre or not isinstance(nombre, str):
            raise DatoInvalidoError("El nombre del repuesto debe ser un texto no vacío.")
        if not proveedor or not isinstance(proveedor, str):
            raise DatoInvalidoError("El proveedor debe ser un texto no vacío.")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise DatoInvalidoError("La cantidad debe ser un entero no negativo.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise DatoInvalidoError("El precio debe ser un número no negativo.")

        self.nombre: str = nombre
        self.proveedor: str = proveedor
        self._cantidad: int = cantidad
        self.precio: float = float(precio)

    def get_cantidad(self) -> int:
        return self._cantidad

    def incrementar_stock(self, cantidad: int) -> None:
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad a incrementar debe ser un entero positivo.")
        self._cantidad += cantidad

    def decrementar_stock(self, cantidad: int) -> None:
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad a decrementar debe ser un entero positivo.")
        if cantidad > self._cantidad:
            raise StockInsuficienteError(
                f"Stock insuficiente de '{self.nombre}'. Disponible: {self._cantidad}, solicitado: {cantidad}"
            )
        self._cantidad -= cantidad

    def __str__(self) -> str:
        return (
            f"Repuesto(nombre='{self.nombre}', proveedor='{self.proveedor}', "
            f"cantidad={self._cantidad}, precio={self.precio:.2f})"
        )


class Almacen(IServiciosCompras, IGestionInventario):

    def __init__(self, nombre: str, localizacion: str) -> None:
        if not nombre or not isinstance(nombre, str):
            raise DatoInvalidoError("El nombre del almacén debe ser un texto no vacío.")
        if not localizacion or not isinstance(localizacion, str):
            raise DatoInvalidoError("La localización del almacén debe ser un texto no vacío.")

        self.nombre: str = nombre
        self.localizacion: str = localizacion
        self._catalogo: dict[str, Repuesto] = {}
        self.comandantes: list[Comandante] = []
        self.operarios: list[OperarioAlmacen] = []

    def alta_comandante(self, comandante: Comandante) -> None:
        if not isinstance(comandante, Comandante):
            raise DatoInvalidoError("Solo se pueden registrar objetos de tipo Comandante.")
        self.comandantes.append(comandante)

    def alta_operario(self, operario: OperarioAlmacen) -> None:
        if not isinstance(operario, OperarioAlmacen):
            raise DatoInvalidoError("Solo se pueden registrar objetos de tipo OperarioAlmacen.")
        self.operarios.append(operario)


    # Implementación de IGestionInventario
    def alta_repuesto(self, operario: OperarioAlmacen, repuesto: Repuesto) -> None:
        
        if operario not in self.operarios:
            raise UsuarioNoAutorizadoError(f"El operario '{operario.nombre}' no está registrado en el almacén.")
        if not isinstance(repuesto, Repuesto):
            raise DatoInvalidoError("Solo se pueden dar de alta objetos de tipo Repuesto.")
        
        if repuesto.nombre in self._catalogo:
            existente = self._catalogo[repuesto.nombre]
            existente.incrementar_stock(repuesto.get_cantidad())
        else:
            self._catalogo[repuesto.nombre] = repuesto

    def eliminar_repuesto(self, operario: OperarioAlmacen, nombre_repuesto: str) -> None:
        if operario not in self.operarios:
            raise UsuarioNoAutorizadoError(f"El operario '{operario.nombre}' no está registrado en el almacén.")
        if nombre_repuesto not in self._catalogo:
            raise RepuestoNoEncontradoError(f"No existe el repuesto '{nombre_repuesto}' en el almacén.")
        del self._catalogo[nombre_repuesto]

    def reponer_stock(self, operario: OperarioAlmacen, nombre_repuesto: str, cantidad: int) -> None:
        if operario not in self.operarios:
            raise UsuarioNoAutorizadoError(f"El operario '{operario.nombre}' no está registrado en el almacén.")
        repuesto = self.buscar_repuesto(operario, nombre_repuesto)
        repuesto.incrementar_stock(cantidad)

    def buscar_repuesto(self, operario: OperarioAlmacen, nombre_repuesto: str) -> Repuesto:
        if operario not in self.operarios:
            raise UsuarioNoAutorizadoError(f"El operario '{operario.nombre}' no está registrado en el almacén.")
        if nombre_repuesto not in self._catalogo:
            raise RepuestoNoEncontradoError(f"No existe el repuesto '{nombre_repuesto}' en el almacén.")
        return self._catalogo[nombre_repuesto]

    # Implementación de IServiciosCompras
    def consultar_repuestos(self, comandante: Comandante) -> list[Repuesto]:
        #if comandante not in self.comandantes:
         #   raise UsuarioNoAutorizadoError(f"El comandante '{comandante.nombre}' no está registrado en el almacén.")
        return list(self._catalogo.values())

    def proveer_repuesto(self, comandante: Comandante, nombre_repuesto: str, cantidad: int) -> float:
        if comandante not in self.comandantes:
            raise UsuarioNoAutorizadoError(f"El comandante '{comandante.nombre}' no está registrado en el almacén.")
        repuesto = self.buscar_repuesto(comandante, nombre_repuesto)
        repuesto.decrementar_stock(cantidad)
        return repuesto.precio * cantidad
    
    def solicitar_repuesto(self, comandante: Comandante, nombre_repuesto: str, cantidad: int) -> str:
        if not comandante.nave.admite_repuesto(nombre_repuesto):
            raise RepuestoNoAutorizadoError(
                f"La nave '{comandante.nave.nombre}' no admite el repuesto '{nombre_repuesto}'."
            )

        coste = self.proveer_repuesto(comandante, nombre_repuesto, cantidad)
        return (
            f"Comandante '{comandante.nombre}': compra realizada -> "
            f"{cantidad} unidad(es) de '{nombre_repuesto}' para '{comandante.nave.nombre}'. "
            f"Coste total: {coste:.2f} créditos."
        )        
    
    def __str__(self) -> str:
        return f"Almacén(nombre='{self.nombre}', localización='{self.localizacion}')"


class EstacionEspacial(Nave):
    def __init__(
        self,
        nombre: str,
        catalogo_repuestos: list[str],
        tripulacion: int,
        pasaje: int,
        ubicacion: UbicacionEstacion,
    ) -> None:
        super().__init__(nombre, catalogo_repuestos)

        if not isinstance(tripulacion, int) or tripulacion < 0:
            raise DatoInvalidoError("La tripulación debe ser un entero no negativo.")
        if not isinstance(pasaje, int) or pasaje < 0:
            raise DatoInvalidoError("El pasaje debe ser un entero no negativo.")
        if not isinstance(ubicacion, UbicacionEstacion):
            raise DatoInvalidoError("La ubicación debe ser un valor de UbicacionEstacion.")

        self.tripulacion: int = tripulacion
        self.pasaje: int = pasaje
        self.ubicacion: UbicacionEstacion = ubicacion

    def descripcion(self) -> str:
        return (
            f"Estación Espacial '{self.nombre}' | "
            f"Tripulación={self.tripulacion}, Pasaje={self.pasaje}, "
            f"Ubicación={self.ubicacion.value}"
        )


class NaveEstelar(Nave, UnidadCombate):
    """
    Herencia múltiple:
    - es una Nave
    - es una UnidadCombate
    """

    def __init__(
        self,
        nombre: str,
        catalogo_repuestos: list[str],
        tripulacion: int,
        pasaje: int,
        clase_nave: ClaseNaveEstelar,
        identificador_combate: str,
        clave_transmision: int,
    ) -> None:
        Nave.__init__(self, nombre, catalogo_repuestos)
        UnidadCombate.__init__(self, identificador_combate, clave_transmision)

        if not isinstance(tripulacion, int) or tripulacion < 0:
            raise DatoInvalidoError("La tripulación debe ser un entero no negativo.")
        if not isinstance(pasaje, int) or pasaje < 0:
            raise DatoInvalidoError("El pasaje debe ser un entero no negativo.")
        if not isinstance(clase_nave, ClaseNaveEstelar):
            raise DatoInvalidoError("La clase de nave debe ser un valor de ClaseNaveEstelar.")

        self.tripulacion: int = tripulacion
        self.pasaje: int = pasaje
        self.clase_nave: ClaseNaveEstelar = clase_nave

    def descripcion(self) -> str:
        return (
            f"Nave Estelar '{self.nombre}' | "
            f"Clase={self.clase_nave.value}, Tripulación={self.tripulacion}, "
            f"Pasaje={self.pasaje}, ID combate={self.identificador_combate}"
        )


class CazaEstelar(Nave, UnidadCombate):
    """
    Herencia múltiple:
    - es una Nave
    - es una UnidadCombate
    """

    def __init__(
        self,
        nombre: str,
        catalogo_repuestos: list[str],
        dotacion: int,
        identificador_combate: str,
        clave_transmision: int,
    ) -> None:
        Nave.__init__(self, nombre, catalogo_repuestos)
        UnidadCombate.__init__(self, identificador_combate, clave_transmision)

        if not isinstance(dotacion, int) or dotacion < 0:
            raise DatoInvalidoError("La dotación debe ser un entero no negativo.")

        self.dotacion: int = dotacion

    def descripcion(self) -> str:
        return (
            f"Caza Estelar '{self.nombre}' | "
            f"Dotación={self.dotacion}, ID combate={self.identificador_combate}"
        )