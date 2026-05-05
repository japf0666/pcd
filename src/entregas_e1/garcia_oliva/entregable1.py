from enum import Enum
from abc import ABC


class UbicacionEstacion(Enum):
    # usamos enumeraciones para evitar faltas de ortografía o valores no aceptados
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"


class ClaseNaveEstelar(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"


class CantidadInvalidaError(Exception):
    # permite personalizar más los errores
    pass


class RepuestoNoEncontrado(Exception):
    pass


class UnidadCombateImperial(ABC):
    # es una clase abstracta que sirve como plantilla para cualquier unidad imperial, es abstracta porque no se puede instanciar directamente.
    def __init__(self, identificador: str, clave: int):
        self.identificador = identificador
        self.clave = clave


class Nave(UnidadCombateImperial):
    # heredamos los atributos de la clase abstracta UnidadCombateImperial por herencia
    def __init__(self, identificador: str, clave: int, nombre: str, catalogo: list):
        super().__init__(identificador, clave)
        self.nombre = nombre
        self.catalogo = catalogo


class EstacionEspacial(Nave):
    # se utiliza la herencia otra vez
    def __init__(self, identificador: str, clave: int, nombre: str, catalogo: list, tripulacion: int, pasaje: int, ubicacion: UbicacionEstacion):
        super().__init__(identificador, clave, nombre, catalogo)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion


class NaveEstelar(Nave):
    def __init__(self, identificador: str, clave: int, nombre: str, catalogo: list, tripulacion: int, pasaje: int, clase: ClaseNaveEstelar):
        super().__init__(identificador, clave, nombre, catalogo)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase


class CazaEstelar(Nave):
    def __init__(self, identificador: str, clave: int, nombre: str, catalogo: list, dotacion: int):
        super().__init__(identificador, clave, nombre, catalogo)
        self.dotacion = dotacion


class Repuesto():
    # se crea el repuesto con el atributo cantidad privado
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.setCantidad(cantidad)
        self.precio = precio

    # se crean los métodos para el atributo privado
    def getCantidad(self):
        return self.__cantidad

    def setCantidad(self, cantidad: int):
        if cantidad < 0:
            raise CantidadInvalidaError(
                "Error: La cantidad no puede ser negativa")
        self.__cantidad = cantidad


class Almacen():
    # la clase almacen actua como un contenedor de repuestos
    def __init__(self, nombre: str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo = []

    def buscarRepuesto(self, nombre: str):
        # esta función recorre los repuestos comprobando el nombre del que se busca
        for i in self.catalogo:
            if i.nombre == nombre:
                return i

        raise RepuestoNoEncontrado("Error: El repuesto no ha sido encontrado")

    def addCatalogo(self, repuesto: Repuesto):
        # añade un nuevo repuesto al almacen
        self.catalogo.append(repuesto)


class Usuario(ABC):
    # la clase usuario es abstracta, porque no se va a declarar un usuario normal directamente, sino uno con rol (Comandante, Operario u otros que se puedan añadir)
    def __init__(self, nombre, identificador):
        self.nombre = nombre
        self.identificador = identificador


class Comandante(Usuario):
    # utiliza la herencia de usuario
    def __init__(self, nombre, identificador):
        super().__init__(nombre, identificador)

    def consultarRepuesto(self, almacenes: list, nombre: str, cantidad: int):
        # proporcionamos diferentes almacenes y el repuesto buscado, recorremos todos los almacenes para encontrar las diferentes opciones
        almacenes_validos = []
        for almacen in almacenes:
            try:
                if almacen.buscarRepuesto(nombre) and almacen.buscarRepuesto(nombre).getCantidad() >= cantidad:
                    print(
                        f"Repuesto encontrado. Nombre almacen: {almacen.nombre}\nPrecio/ud: {almacen.buscarRepuesto(nombre).precio} \nPrecio total: {almacen.buscarRepuesto(nombre).precio * cantidad}\n")
                    almacenes_validos.append(almacen)
            except:
                continue

        if not almacenes_validos:
            print("No se ha encontrado el repuesto en ningún almacen")
        return almacenes_validos

    def adquirirRepuesto(self, almacen: Almacen, nombre: str, cantidad: int):
        # una vez encontrado el alamacen con el repuesto, se puede utilizar está función para adquirirlo y actualizar la cantidad
        repuesto = almacen.buscarRepuesto(nombre)
        uds = repuesto.getCantidad()
        repuesto.setCantidad(uds - cantidad)


class Operario(Usuario):
    def __init__(self, nombre, identificador):
        super().__init__(nombre, identificador)

    def modificarRepuesto(self, almacen: Almacen, nombre: str, cantidad: int, precio: float):
        # esta función permite al operario cambiar los valores de un repuesto
        repuesto = almacen.buscarRepuesto(nombre)
        repuesto.nombre = nombre
        repuesto.setCantidad(cantidad)
        repuesto.precio = precio

    def anadirRepuesto(self, almacen: Almacen, nombre: str, proveedor: str, cantidad: int, precio: float):
        # esta función permite al operario añadir nuevos repuestos a almacenes
        repuesto = Repuesto(nombre, proveedor, cantidad, precio)
        almacen.addCatalogo(repuesto)


if __name__ == "__main__":
    almacen_central = Almacen("Almacen Central", "Endor")
    print("Almacen Central creado")
    repuesto1 = Repuesto("Diodos del Lado Izquierdo",
                         "Astilleros de Magrathea", 10, 29.0)
    repuesto2 = Repuesto("Trazador de Vectores Atómicos Sub-Mesónico",
                         "Compañía Cibernética Sirius", 20, 199.0)
    print("Respuestos creados")
    almacen_central.addCatalogo(repuesto1)
    almacen_central.addCatalogo(repuesto2)
    print("Repuestos añadidos al almacen central")

    repuesto_buscado1 = almacen_central.buscarRepuesto(
        "Trazador de Vectores Atómicos Sub-Mesónico")
    print(f"Repuesto: {repuesto_buscado1.nombre}")

    estacion_espacial = EstacionEspacial(
        "d1ad5rf", 489214, "Just Read The Instructions", ["Diodos del Lado Izquierdo"], 500, 300, UbicacionEstacion.NEBULOSA_KALIIDA)
    print("Estación espacial creada")
    print(
        f"Nombre: {estacion_espacial.nombre}\nIdentificador: {estacion_espacial.identificador}\nUbicación: {estacion_espacial.ubicacion}\n")
    nave_estelar = NaveEstelar("f4ahdfa", 8527121, "Of Course I Still Love You", [
                               "Trazador de Vectores Atómicos Sub-Mesónico"], 100, 80, ClaseNaveEstelar.ECLIPSE)
    print("Nave estelar creada")
    print(
        f"Nombre: {nave_estelar.nombre}\nIdentificador: {nave_estelar.identificador}\nClase: {nave_estelar.clase}\n")
    caza_estelar = CazaEstelar("nc4z473", 69042012, "Size Isn't Everything", [
                               "Diodos del Lado Izquierdo", "Trazador de Vectores Atómicos Sub-Mesónico"], 3)
    print("Caza estelar creado")
    print(
        f"Nombre: {caza_estelar.nombre}\nIdentificador: {caza_estelar.identificador}\n")

    operario1 = Operario("TK-421", "OP-8821")
    print("Operario creado")
    print(
        f"Nombre: {operario1.nombre}\nIdentificador: {operario1.identificador}\n")

    comandante1 = Comandante("Thrawn", "CMD-7734")
    print("Comandante creado")
    print(
        f"Nombre: {comandante1.nombre}\nIdentificador: {comandante1.identificador}\n")

    print("[+] Pruebas de acciones de Operario")
    operario1.anadirRepuesto(
        almacen_central, "Cristal Kyber", "Ilum Corp", 5, 50000.0)
    print("Repuesto 'Cristal Kyber' añadido al almacen por el operario.")

    operario1.modificarRepuesto(
        almacen_central, "Diodos del Lado Izquierdo", 15, 29.0)
    stock_actualizado = almacen_central.buscarRepuesto(
        "Diodos del Lado Izquierdo").getCantidad()
    print(
        f"Repuesto modificado por el operario. Nueva cantidad de Diodos: {stock_actualizado}\n")

    print("[+] Pruebas de acciones de Comandante")
    print("El comandante consulta stock de 2 Trazadores:")
    lista_almacenes = [almacen_central]
    almacenes_con_stock = comandante1.consultarRepuesto(
        lista_almacenes, "Trazador de Vectores Atómicos Sub-Mesónico", 2)

    if almacenes_con_stock:
        comandante1.adquirirRepuesto(
            almacen_central, "Trazador de Vectores Atómicos Sub-Mesónico", 2)
        stock_restante = almacen_central.buscarRepuesto(
            "Trazador de Vectores Atómicos Sub-Mesónico").getCantidad()
        print(
            f"El comandante ha adquirido el repuesto. Cantidad restante en almacén: {stock_restante}\n")

    print("[+] Pruebas de gestión de Excepciones")
    try:
        print("Intentando crear un repuesto con cantidad negativa...")
        repuesto_erroneo = Repuesto(
            "Panel Solar Defectuoso", "Kuat", -5, 100.0)
    except CantidadInvalidaError as e:
        print(f"Excepción capturada con éxito: {e}")

    try:
        print("\nIntentando buscar un repuesto que no existe en el almacén...")
        almacen_central.buscarRepuesto("Motor Hiperimpulsor Inexistente")
    except RepuestoNoEncontrado as e:
        print(f"Excepción capturada con éxito: {e}\n")
