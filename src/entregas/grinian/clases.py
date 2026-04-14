from abc import ABC
from enums import *
from excepciones import *


class Repuesto:

    """
    Clase Repuesto

    Representa una pieza física dentro del sistema logístico.

    Atributos:
        nombre -> string
        proveedor -> string
        __cantidad -> int
            cantidad de stock disponible de la pieza (privado, no admite negativos)
        coste -> float
            precio unitario del repuesto (no admite negativos)
    """

    def __init__(self, nombre: str, proveedor: str, cantidad: int, coste: float):
        self.nombre = nombre
        self.proveedor = proveedor

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad 

        if coste < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.coste = coste

    # --getters--
    def get_nombre(self) -> str:
        return self.nombre
    
    def get_proveedor(self) -> str:
        return self.proveedor
    
    def get_coste(self) -> float:
        return self.coste

    def get_cantidad(self) -> int:
        return self.__cantidad


    # --seters--
    def set_nombre(self,nombre:str):
        self.nombre = nombre

    def set_proveedor(self,proveedor: str):
        self.proveedor = proveedor

    def set_coste(self,coste:float):
        if coste < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.coste = coste

    def set_cantidad(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad

    def __str__(self):
        return f"el repuesto con nombre:{self.get_nombre()} y cantidad {self.get_cantidad()}"

class Almacen:

    """
    Clase Almacen

    Representa una instalación física donde se guardan las piezas del Imperio.

    Atributos:
        nombre -> str
        localizacion -> str
        catalogo_piezas -> []
            Lista que guarda los objetos de tipo Repuesto disponibles en este almacén.

    Métodos:
        agregar_repuesto():
            Añade un objeto Repuesto nuevo a la lista del catálogo.
        buscar_repuesto():
            Busca una pieza por su nombre dentro del catálogo y devuelve el objeto (o -1 si no está).
    """

    def __init__(self, nombre: str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo_piezas = [] 


    #geters 
    def get_nombre(self):
        return self.nombre
    
    def get_localizacion(self):
        return self.localizacion

    def get_catalogo(self):
        return self.catalogo_piezas

    #setters

    def set_nombre(self, nombre:str):
        self.nombre = nombre

    def set_localizacion(self,localizacion:str):
        self.localizacion = localizacion

    #metodos 
    def agregar_repuesto(self, repuesto: Repuesto):

        #agrega al catalogo de repuestos un objeto repuesto
        self.catalogo_piezas.append(repuesto)

    def buscar_repuesto(self, nombre: str) -> Repuesto:
        """
        El metodo busca dentro del catalogo si existe 
        el repuesto que se se esta buscando

        busca por el nombre no por el objeto

        si no lo encuentra devuelve un -1
        """

        for repuesto in self.get_catalogo():
            if repuesto.get_nombre() == nombre:
                return repuesto
        return (-1)
    
    def __str__(self):
        return f"{self.get_nombre()}"
    
class Nave(ABC):

    """
    Clase Nave

    Atributos:
        nombre -> string
        Repuestos -> []
            Repuestos es una lista de que contiene
            los diferentes tipos de repuestos dentro
            de una nave (la lista son de objetos tipo string 
            por lo que seran los nombres)

    Metodos
        mostrar_informacion():
            devuelve un string con la informacion basica de la nave
        añadir_repuestos():
            el metodo añade a la lista un repuesto nuevo
    """

    def __init__(self, nombre:str,**kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self.repuestos = []

    #getter

    def get_nombre(self):
        return self.nombre

    def get_repuestos(self):
        return self.repuestos
    
    #setter

    def set_nombre(self,nombre:str):
        self.nombre = nombre

    #metodos

    def mostrar_informacion(self):
        return f"Nombre de nave: {self.get_nombre}\nNumero de repuestos: {len(self.get_repuestos())}"


    def añadir_repuestos(self,repuesto:str):

        # REVISAR PQ NO CUADRA QUE SEA UN STR PARA TEMA DUPLICADOS

        self.get_repuestos().append(repuesto)

class UnidadCombate(ABC):

    """
    Clase abstracta UnidadCombate

    Define las características básicas de combate y comunicaciones para las naves.

    Atributos:
        identificador -> str
            código único de la nave (ej. ID-001)
        clave_transmision -> int
            PIN secreto numérico para recibir mensajes seguros
        mensajes_recibidos -> []
            lista de strings que funciona como bandeja de entrada

    Métodos:
        recibir_mensaje():
            guarda el texto del mensaje entrante en la lista
        leer_mensajes():
            devuelve la lista con todos los mensajes guardados
    """

    def __init__(self, identificador:str,clave_transmision:int, **kwargs):
        super().__init__(**kwargs)
        self.identificador = identificador
        self.clave_transmision = clave_transmision
        self.mensajes_recibidos = []

    #geters

    def get_identificador(self):
        return self.identificador
    
    def get_clave_transmision(self):
        return self.clave_transmision
    
    #setters

    def set_identificador(self, identificador:str):
        self.identificador = identificador

    def set_clave_transmision(self, clave_transmision:int):
        self.clave_transmision = clave_transmision

    #metodos
    def recibir_mensaje(self, mensaje: str):

        # recibe el mensaje como metodo y lo mete a la lista de mensajes
        self.mensajes_recibidos.append(mensaje)

    def leer_mensajes(self):
        #devuelve la lista de mensajes
        return self.mensajes_recibidos
    

class NaveEstelar(Nave, UnidadCombate):

    """
    Clase NaveEstelar

    Hereda de Nave y UnidadCombate. Representa una nave de la flota operativa.

    Atributos:
        tripulacion -> int
            número de tripulantes necesarios para operar la nave
        pasaje -> int
            capacidad para transportar tropas o pasajeros extra
        clase -> EClaseNave
            categoría de la nave basada en el Enum (ej. EJECUTOR)
        (Hereda nombre, identificador y clave_transmision de sus padres)

    Métodos:
        get_clave():
            devuelve la clave de transmisión (unificando el acceso para el sistema de mensajes)
    """

    def __init__(self, nombre: str, identificador: str, clave_transmision: int, tripulacion: int, pasaje: int, clase: EClaseNave):
        super().__init__(nombre=nombre, identificador=identificador, clave_transmision=clave_transmision)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def get_tripulacion(self) -> int:
        return self.tripulacion

    def get_pasaje(self) -> int:
        return self.pasaje

    def get_clase(self) -> EClaseNave:
        return self.clase

    def get_clave(self) -> int:
        return self.clave_transmision
    
    # --setters--
    def set_tripulacion(self, tripulacion: int):
        self.tripulacion = tripulacion

    def set_pasaje(self, pasaje: int):
        self.pasaje = pasaje

    def set_clase(self, clase: EClaseNave):
        self.clase = clase

class EstacionEspacial(Nave, UnidadCombate):

    """
    Clase EstacionEspacial

    Hereda de Nave y UnidadCombate. Representa una base orbital o instalación fija en el espacio.

    Atributos:
        tripulacion -> int
            número de tripulantes necesarios para mantener operativa la estación
        pasaje -> int
            capacidad máxima para alojar tropas o visitantes
        ubicacion -> EUbicacion
            sector espacial o planeta donde está anclada basada en el Enum (ej. ENDOR)
        (Hereda nombre, identificador y clave_transmision de sus padres)

    Métodos:
        get_clave():
            devuelve la clave de transmisión para el sistema de comunicaciones
    """

    def __init__(self, nombre: str, identificador: str, clave_transmision: int, tripulacion: int, pasaje: int, ubicacion: EUbicacion):
        super().__init__(nombre=nombre, identificador=identificador, clave_transmision=clave_transmision)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion


    def get_tripulacion(self) -> int:
        return self.tripulacion

    def get_pasaje(self) -> int:
        return self.pasaje

    def get_ubicacion(self) -> EUbicacion:
        return self.ubicacion

    def get_clave(self) -> int:
        return self.clave_transmision

    def set_tripulacion(self, tripulacion: int):
        self.tripulacion = tripulacion

    def set_pasaje(self, pasaje: int):
        self.pasaje = pasaje

    def set_ubicacion(self, ubicacion: EUbicacion):
        self.ubicacion = ubicacion

class CazaEstelar(Nave, UnidadCombate):
    
    """
    Clase CazaEstelar

    Hereda de Nave y UnidadCombate. Representa una nave de combate ligera o de asalto rápido.

    Atributos:
        dotacion -> int
            número de pilotos o tripulantes mínimos que operan el caza
        (Hereda nombre, identificador y clave_transmision de sus padres)

    Métodos:
        get_clave():
            devuelve la clave de transmisión para la radio de la flota
    """


    def __init__(self, nombre: str, identificador: str, clave_transmision: int, dotacion: int):
        super().__init__(nombre=nombre, identificador=identificador, clave_transmision=clave_transmision)
        self.dotacion = dotacion

    def get_dotacion(self) -> int:
        return self.dotacion

    def get_clave(self) -> int:
        return self.clave_transmision

    def set_dotacion(self, dotacion: int):
        self.dotacion = dotacion

class Usuario(ABC):

    """
    Clase abstracta Usuario

    Define la estructura base para cualquier persona con acceso al sistema (Comandantes, Operarios, Admins).

    Atributos:
        ID -> str
            código único de identificación para iniciar sesión (ej. CMD-01)
        nombre -> str
            nombre real o designación del usuario dentro del Imperio
    """

    def __init__(self,ID:str,nombre:str):
        self.ID = ID
        self.nombre=nombre

    def get_ID(self):

        return self.ID
    
    def get_nombre(self):
        return self.nombre


class Comandante(Usuario):

    """
    Clase Comandante

    Hereda de Usuario. Representa a un oficial imperial al mando de una nave de la flota.

    Atributos:
        nave -> Nave
            objeto de la clase Nave que este comandante tiene asignada
        (Hereda ID y nombre de la clase padre)
    """

    def __init__(self, ID, nombre,nave:Nave):
        super().__init__(ID, nombre)
        self.nave = nave

    def get_nave(self):
        return self.nave
    
    def set_nave(self,nave:Nave):
        self.nave = nave

class Operario(Usuario):

    """
    Clase Operario

    Hereda de Usuario. Representa al personal logístico encargado de gestionar el inventario de piezas.

    Atributos:
        almacen -> Almacen
            objeto de la clase Almacen donde este operario tiene su puesto de trabajo
        (Hereda ID y nombre de la clase padre)
    """

    def __init__(self, ID, nombre,almacen:Almacen):
        super().__init__(ID, nombre)
        self.almacen = almacen

    def get_almacen(self):
        return self.almacen
    
    def set_almacen(self, almacen:Almacen):
        self.almacen = almacen

class Admin(Usuario):
    def __init__(self, ID, nombre):
        super().__init__(ID, nombre)