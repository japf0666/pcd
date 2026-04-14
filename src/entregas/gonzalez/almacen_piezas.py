from __future__ import annotations  
from excepciones import PermisoDenegadoError, CantidadError
from naves import Nave  

class Repuesto:
    def __init__(self, nombre: str, proovedor: str, cantidad: int, precio: float):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacío")
        if not isinstance(proovedor, str) or not proovedor.strip():
            raise ValueError("El proveedor debe ser un texto no vacío")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un número entero no negativo")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número no negativo")

        self.nombre = nombre
        self._cantidad = cantidad
        self.proovedor = proovedor
        self.precio = precio

    # obtenemos la cantidad del repuesto
    def get_cantidad(self) -> int:
        return self._cantidad

    # Aumentamos la cantidad de un repuesto
    def añadir_cantidad(self, cantidad: int):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a añadir debe ser un número entero positivo")
        self._cantidad += cantidad

    # Reducimos la cantidad de el repuesto
    def reducir_cantidad(self, cantidad: int):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a reducir debe ser un número entero positivo")
        if cantidad > self._cantidad:
            raise ValueError(f"No se puede reducir más de la cantidad disponible ({self._cantidad})")
        self._cantidad -= cantidad

    # Cambiamos el precio del repuesto
    def cambiar_precio(self, nuevo_precio: float | int):
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio < 0:
            raise ValueError("El nuevo precio debe ser un número no negativo")
        self.precio = nuevo_precio

    # Mostramos información del repuesto con con un print()
    def __str__(self):
        return (f"Repuesto '{self.nombre}' del proveedor '{self.proovedor}' "
                f"con cantidad {self._cantidad} y precio {self.precio}")


class OperarioAlmacen:
    def __init__(self, nombre: str):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacío")
        self.nombre = nombre

    def añadir_repuesto(self, repuesto: Repuesto, almacen: Almacen):
        if not isinstance(repuesto, Repuesto):
            raise ValueError("El repuesto debe ser una instancia de Repuesto")
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        # Utilizamos el metodo de añadir_repuesto implementado en la clase almacen
        almacen.añadir_repuesto(repuesto, self)
        print(f"El operario '{self.nombre}' ha añadido el repuesto '{repuesto.nombre}' al almacén '{almacen.id_nombre}'")

    def retirar_repuesto(self, repuesto: Repuesto, almacen: Almacen):
        """Elimina completamente un repuesto del catálogo."""
        if not isinstance(repuesto, Repuesto):
            raise ValueError("El repuesto debe ser una instancia de Repuesto")
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        # Utilizamos el metodo de eliminar_repuesto implementado en la clase almacen
        almacen.eliminar_repuesto(repuesto, self)
        print(f"El operario '{self.nombre}' ha retirado el repuesto '{repuesto.nombre}' del almacén '{almacen.id_nombre}'")

    def buscar_repuesto(self, repuesto_nom: str, almacen: Almacen):
        if not isinstance(repuesto_nom, str) or not repuesto_nom.strip():
            raise ValueError("El nombre del repuesto debe ser un texto no vacío")
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        # Utilizamos el metodo de buscar_repuesto implementado en la clase almacen
        # para obtener el repuesto y mostrar su información si existe y devolverlo
        repuesto = almacen.buscar_repuesto(repuesto_nom, self)
        if repuesto:
            print(f"El repuesto '{repuesto_nom}' está disponible en el almacén '{almacen.id_nombre}' "
                  f"a un precio de {repuesto.precio} con una cantidad de {repuesto.get_cantidad()}")
            return repuesto

    def cambiar_precio_repuesto(self, repuesto_nom: str, nuevo_precio: float, almacen: Almacen):
        if not isinstance(repuesto_nom, str) or not repuesto_nom.strip():
            raise ValueError("El nombre del repuesto debe ser un texto no vacío")
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio <= 0:
            raise ValueError("El nuevo precio debe ser un número positivo")
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        # actualizamos el precio del repuesto con un metodo de la clase almacén
        almacen.actualizar_precio_repuesto(repuesto_nom, nuevo_precio, self)

    def reponer_repuesto(self, repuesto_nom: str, cantidad: int, almacen: Almacen):
        """Aumenta la cantidad de un repuesto ya existente en el catálogo."""
        if not isinstance(repuesto_nom, str) or not repuesto_nom.strip():
            raise ValueError("El nombre del repuesto debe ser un texto no vacío")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un número entero positivo")
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        # actualizamos la cantidad del repuesto con un método de la clase almacén
        almacen.actualizar_cantidad_repuesto(repuesto_nom, cantidad, self)

    # Mostrammos información del operario con un print()
    def __str__(self):
        return f"OperarioAlmacen '{self.nombre}'"


class Comandante:
    def __init__(self, nombre: str, nave: Nave):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacío")
        if not isinstance(nave, Nave):
            raise ValueError("La nave debe ser una instancia de Nave")
        self.nombre = nombre
        self.nave = nave
        # Le asignamos a la nave correspondiente el comandante con un método de la clase nave
        nave._asignar_comandante(self)

    def consultar_repuesto(self, nombre_repuesto: str, almacen: Almacen):
        """Consulta la disponibilidad de un repuesto en un almacén."""
        if not isinstance(nombre_repuesto, str) or not nombre_repuesto.strip():
            raise ValueError("El nombre del repuesto debe ser un texto no vacío")
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        # Utilizamos el método de consultar_repuesto implementado en la clase almacén
        almacen.consultar_repuesto(nombre_repuesto, self)

    def adquirir_repuesto(self, nombre_repuesto: str, cantidad: int, almacen: Almacen):
        """Adquiere (reduce del stock) una cantidad de un repuesto."""
        if not isinstance(nombre_repuesto, str) or not nombre_repuesto.strip():
            raise ValueError("El nombre del repuesto debe ser un texto no vacío")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un número entero positivo")
        if not isinstance(almacen, Almacen):
            raise ValueError("El almacén debe ser una instancia de Almacen")
        # Utilizamos el método de adquirir_repuesto implementado en la clase almacén
        almacen.adquirir_repuesto(nombre_repuesto, cantidad, self)

    # mostramos información del comandante con un print()
    def __str__(self):
        return f"Comandante '{self.nombre}' de la nave '{self.nave}'"


class Almacen:
    def __init__(self, id_nombre: str, localizacion: str):
        if not isinstance(id_nombre, str) or not id_nombre.strip():
            raise ValueError("El id_nombre debe ser un texto no vacío")
        if not isinstance(localizacion, str) or not localizacion.strip():
            raise ValueError("La localización debe ser un texto no vacío")

        self.id_nombre = id_nombre
        self.localizacion = localizacion
        # Utilizamos un diccionario para acceder por string
        self.catalogo_piezas: dict[str, Repuesto] = {}  # nombre : Repuesto
        self.operarios: list[OperarioAlmacen] = []
        self.comandantes: list[Comandante] = []

    # ── Métodos de gestión de personal ──────────────────────────────────────

    def añadir_operario(self, operario: OperarioAlmacen):
        if not isinstance(operario, OperarioAlmacen):
            raise ValueError("El operario debe ser una instancia de OperarioAlmacen")
        if operario in self.operarios:
            raise ValueError("El operario ya se encuentra en la lista de operarios")
        # añadimos a la lista al operario
        self.operarios.append(operario)

    def añadir_comandante(self, comandante: Comandante):
        if not isinstance(comandante, Comandante):
            raise ValueError("El comandante debe ser una instancia de Comandante")
        if comandante in self.comandantes:
            raise ValueError("El comandante ya se encuentra en la lista de comandantes")
        # añadimos a la lista al comandante
        self.comandantes.append(comandante)

    # ── Métodos para OperarioAlmacen ────────────────────────────────────────

    def añadir_repuesto(self, repuesto: Repuesto, operario: OperarioAlmacen):
        if not isinstance(repuesto, Repuesto):
            raise ValueError("El repuesto debe ser una instancia de Repuesto")
        if operario not in self.operarios:
            raise PermisoDenegadoError("El operario no tiene permiso para añadir repuestos en este almacén")

        if repuesto.nombre in self.catalogo_piezas:
            # si ya existe ese repuesto, le añadimos a la cantidad la nueva cantidad de repuesto
            self.buscar_repuesto(repuesto.nombre, operario).añadir_cantidad(repuesto.get_cantidad())
        else:
            # si no existe, creamos un clave nueva en el diccionario con el repuesto
            self.catalogo_piezas[repuesto.nombre] = repuesto

    def eliminar_repuesto(self, repuesto: Repuesto, operario: OperarioAlmacen):
        if not isinstance(repuesto, Repuesto):
            raise ValueError("El repuesto debe ser una instancia de Repuesto")
        if operario not in self.operarios:
            raise PermisoDenegadoError("El operario no tiene permiso para eliminar repuestos en este almacén")
        # si no esta en el catalogo lanzamos un error
        if repuesto.nombre not in self.catalogo_piezas:
            raise ValueError("El repuesto no se encuentra en el catálogo")
        # eliminamos la clave del repuesto del diccionario
        del self.catalogo_piezas[repuesto.nombre]

    def buscar_repuesto(self, nombre_repuesto: str, buscador: OperarioAlmacen|Comandante):        
        if not buscador in self.operarios and not buscador in self.comandantes:
            raise PermisoDenegadoError("El buscador no tiene permiso para buscar repuestos en este almacén")
        
        repuesto = self.catalogo_piezas.get(nombre_repuesto)
        # en caso de que no este lanzamos un error, si esta lo devolvemos 
        if repuesto is None:
            raise ValueError(f"El repuesto '{nombre_repuesto}' no se encuentra en el catálogo del almacén")
        return repuesto

    def actualizar_cantidad_repuesto(self, nombre_repuesto: str, cantidad: int, operario: OperarioAlmacen):
        """Repone (aumenta) la cantidad de un repuesto existente."""
        if operario not in self.operarios:
            raise PermisoDenegadoError("El operario no tiene permiso para actualizar la cantidad de repuestos en este almacén")
        if nombre_repuesto not in self.catalogo_piezas:
            raise ValueError("El repuesto no se encuentra en el catálogo")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadError("La cantidad a reponer debe ser un entero positivo")
        # añadimos la cantidad al respuesto, si no esta ya se encarga buscar_repuesto de lanzar un error
        self.buscar_repuesto(nombre_repuesto, operario).añadir_cantidad(cantidad)

    def actualizar_precio_repuesto(self, nombre_repuesto: str, nuevo_precio: float | int, operario: OperarioAlmacen):
        if operario not in self.operarios:
            raise PermisoDenegadoError("El operario no tiene permiso para actualizar el precio de repuestos en este almacén")
        if nombre_repuesto not in self.catalogo_piezas:
            raise ValueError("El repuesto no se encuentra en el catálogo")
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio < 0:
            raise ValueError("El nuevo precio debe ser un número no negativo")
        # actualizamos el precio del repuesto, si no esta ya se encarga buscar_repuesto de lanzar un error
        self.buscar_repuesto(nombre_repuesto, operario).cambiar_precio(nuevo_precio)

    # ── Métodos para Comandante ─────────────────────────────────────────────
    def consultar_repuesto(self, nombre_repuesto: str, comandante: Comandante):
        if comandante not in self.comandantes:
            raise PermisoDenegadoError("El comandante no tiene permiso para consultar repuestos en este almacén")
        # buscamos el respuesto, si esta mostramos la informacion 
        repuesto = self.buscar_repuesto(nombre_repuesto, comandante)
        if repuesto:
            print(f"El repuesto '{repuesto.nombre}' está disponible en el almacén '{self.id_nombre}' "
                  f"a un precio de {repuesto.precio} con una cantidad de {repuesto.get_cantidad()}")
        else:
            raise ValueError(f"El repuesto '{nombre_repuesto}' no se encuentra en el catálogo del almacén")

    def adquirir_repuesto(self, nombre_repuesto: str, cantidad: int, comandante: Comandante):
        if comandante not in self.comandantes:
            raise PermisoDenegadoError("El comandante no tiene permiso para adquirir repuestos en este almacén")
        if nombre_repuesto not in self.catalogo_piezas:
            raise ValueError("El repuesto no se encuentra en el catálogo")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadError("La cantidad a adquirir debe ser un entero positivo")
        # buscamos el respuesto, si esta reducimos la cantidad y mostramos informacion, 
        # si no esta ya se encarga buscar_repuesto de lanzar un error
        repuesto = self.buscar_repuesto(nombre_repuesto, comandante)
        if cantidad > repuesto.get_cantidad():
            raise CantidadError("No se puede adquirir más de la cantidad disponible")
        repuesto.reducir_cantidad(cantidad)
        print(f"El comandante '{comandante.nombre}' ha adquirido {cantidad} unidades de '{repuesto.nombre}' "
              f"por un precio total de {cantidad * repuesto.precio}")
    # mostramos información del almacén con un print()
    def __str__(self):
        return (f"Almacén '{self.id_nombre}' ubicado en '{self.localizacion}' "
                f"con {len(self.catalogo_piezas)} repuestos, "
                f"{len(self.operarios)} operarios y {len(self.comandantes)} comandantes")

    def mostrar_repuestos(self):
        if not self.catalogo_piezas:
            print(f"El almacén '{self.id_nombre}' no tiene repuestos en su catálogo.")
        else:
            print(f"Repuestos en el almacén '{self.id_nombre}':")
            # mostramos la informacion de cada repuesto
            for repuesto in self.catalogo_piezas.values():
                print(repuesto)