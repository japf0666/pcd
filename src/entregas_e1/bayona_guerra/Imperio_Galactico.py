from enum import Enum
from abc import ABCMeta, abstractmethod

class EUbicacion(Enum):
    '''Enumeramos las ubicaciones en las que se puede situar las 
    Estaciones Espaciales'''
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cumulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class EClaseNave(Enum):
    '''Enumeramos las clases a las que pueden pertenecer las naves 
    estelares'''
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

class AccesoDenegado(Exception):
    '''Creamos una excepcion para cuando se utilice una clave que no esta
    autentificada en una unidad de combatw '''
    pass

class EmptyError(Exception):
    '''Creamos una excepcion para cuando nos encontremos una lista vacia'''
    pass

class StockError(Exception):
    '''Creamos una excepcion para cuando busquemos un repuesto que NO se 
    encuentre en Stock'''
    pass

class RepuestoInexistente(Exception):
    '''Creamos una excepcion para cuando se solicite un repuesto que NO se
    encuentre en la lista de piezas de una nave'''
    pass

class UnidadCombate(metaclass=ABCMeta):
    '''Clase abstracta que modela las distintas unidades de combate que 
    se encuentran en el Imperio Galactico. Contiene el id de la unidad de
    combate y una clave cifrada que se usara para enviar mensajes'''

    def __init__(self, idCombate:str, claveCifrada:int):
        '''Comprobamos que el tipo de dato introducido es correcto'''
        if not isinstance(idCombate, str):
            raise TypeError("idCombate debe ser una cadena de texto")
        
        if not isinstance(claveCifrada, int):
            raise TypeError("claveCifrada debe ser un numero entero")

        self._idCombate = idCombate
        self._claveCifrada = claveCifrada

    def autentificarClave(self, clave_a_verificar:int)->bool:
        '''Esta funcion toma una clave y comprueba si coincide con la 
        clave cifrada. Si es asi, devuelve True'''

        '''Comprobamos que el tipo de dato introducido es correcto'''
        if not isinstance(clave_a_verificar, int):
            raise TypeError("clave_a_verificar debe ser un numero entero")
        
        if clave_a_verificar == self._claveCifrada:
            print(f'CLAVE CORRECTA.\nUnidad de Combate {self._claveCifrada} autentificada correctamente')
            return True
        
        raise AccesoDenegado('CLAVE INCORRECTA.\nRevise la clave introducida')

    @abstractmethod
    def transmitirMensaje(self, mensaje:str, clave:int)->None:
        '''Esta funcion toma un mensaje y una clave y la muestra. Al ser un
        metodo abstracto, los hijos se encargaran de mostrar el mensaje por 
        pantalla'''

        '''Comprobamos que el tipo de dato introducido es correcto'''
        if not isinstance(mensaje, str):
            raise TypeError("mensaje debe ser una cadena de texto")
        
        if not isinstance(clave, int):
            raise TypeError("clave debe ser un numero entero")
        
        if self.autentificarClave(clave):
            '''Esta condicion se cumplira si la clave introducioda coincide con
            la clave cifrada de la unidad de combate'''
            pass

class Repuesto:
    '''Clase que modela los repuestos de lan distintas naves del Imperio 
    Galactico. Contiene el nombre del repuesto, el proveedor, la cantidad
    que hay de estos y el precio por unidad'''

    def __init__(self, nombre:str, proveedor:str, cantidad:int, precio:float):
        '''Comprobamos que el tipo de dato introducido es correcto'''
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        if not isinstance(proveedor, str):
            raise TypeError("proveedor debe ser una cadena de texto")
        
        if not isinstance(cantidad, int):
            raise TypeError("cantidad debe ser un numero entero")
        
        if not isinstance(precio, (int, float)):
            raise TypeError("precio debe ser un numero")
        
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio
    
    def obtenerUnidades(self)->int:
        '''Esta funcion devuelve el numero de unidades del repuesto'''
        return self.__cantidad
    
    def aumentarStock(self, cantidad_aumentar:int)->None:
        '''Esta funcion se encarga de aumentar el numero de unidades existentes
        del repuesto'''

        '''Comprobamos que el tipo de dato introducido es correcto'''
        if not isinstance(cantidad_aumentar, int):
            raise TypeError("cantidad_aumentar debe ser un entero")
        
        self.__cantidad += cantidad_aumentar

    def reducirStock(self, cantidad_disminuir:int)->None:
        '''Esta funcion se encarga de disminuir el numero de unidades existentes
        del repuesto'''

        '''Comprobamos que el tipo de dato introducido es correcto'''
        if not isinstance(cantidad_disminuir, int):
            raise TypeError("cantidad_disminuir debe ser un numero entero")
        
        if cantidad_disminuir > self.__cantidad:
            raise ValueError("La cantidad a disminuir es mayor que la cantidad actual en stock")
    
        self.__cantidad -= cantidad_disminuir

class Nave(UnidadCombate, metaclass=ABCMeta):
    '''Clase abstracta hija de la clase UnidadCombate que modela los distintos
    tipos de naves existentes en el Imperio Galactico. Al ser una clase hija
    de UnidadCombate, esta hereda todos los atributos del padre y añade los
    atributos referentes al nombre y al catalogo de piezas de repuesto'''

    def __init__(self, idCombate, claveCifrada, nombre:str, catalogoPiezas:list[str]):
        '''Comprobamos que el tipo de dato introducido es correcto'''
        super().__init__(idCombate, claveCifrada)
        self._nombre = nombre
        self._catalogoPiezas = catalogoPiezas
        self.__repuestos_solicitados = {}

    @abstractmethod
    def transmitirMensaje(self, mensaje: str, clave:int)->None:
        '''Esta funcion toma un mensaje y una clave y la muestra. Al ser un
        metodo abstracto, los hijos se encargaran de mostrar el mensaje por 
        pantalla'''

        super().transmitirMensaje(mensaje, clave)

    def consultarCatalogo(self)->list[str]:
        '''Esta funcion se encarga de devolver el catalogo de piezas de repuesto
        de la nave'''

        '''Comprobamos que el tipo de dato introducido es correcto'''
        if len(self._catalogoPiezas) == 0:
            raise EmptyError("El catalogo esta vacio")
        
        return self._catalogoPiezas
    
    def solicitarRepuesto(self, repuesto:Repuesto, cantidad:int)->None:
        '''Esta funcion se encarga de solicitar un repuesto de una pieza
        que se encuentre en el catalogo de piezas de la nave'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto debe ser un objeto de la clase Repuesto")
        
        if not isinstance(cantidad, int):
            raise TypeError("cantidad debe ser un numero entero")
        
        if cantidad > repuesto.obtenerUnidades():
            raise ValueError("La cantidad solicitada es mayor a la existente en stock")        
        
        if repuesto.nombre not in self._catalogoPiezas:
            raise RepuestoInexistente(f"{repuesto.nombre} NO se encuentra en el catalogo de piezas")

        self.__repuestos_solicitados[repuesto.nombre] = cantidad
        repuesto.reducirStock(cantidad)

        print("Repuesto solicitado con exito")

class EstacionEspacial(Nave):
    '''Clase hija de la clase Nave, la cual, a parte de heredar los atributos
    del padre, posee los atributos de tripulacion, pasaje y ubicacion'''

    '''Comprobamos que el tipo de dato introducido es correcto'''

    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, tripulacion:int, pasaje:int, ubicacion:EUbicacion):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        if not isinstance(tripulacion, int):
            raise TypeError("tripulacion debe ser un numero entero")
        
        if not isinstance(pasaje, int):
            raise TypeError("pasaje debe ser un numero entero")
        
        if not isinstance(ubicacion, EUbicacion):
            raise TypeError("ubicacion debe estar contenido en la enumeracion referente a las ubicaciones")
        
        if tripulacion < 0:
            raise ValueError("tripulacion debe ser positivo")
        
        if pasaje < 0:
            raise ValueError("pasaje debe ser positivo")
        
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__ubicacion = ubicacion

    def calcularCapacidad(self)->int:
        '''Esta funcion se encarga sumar el numero de miembros de la 
        tripulacion con el pesaje'''
        capacidad_total = self.__tripulacion + self.__pasaje
        return capacidad_total
    
    def actualizarUbicacion(self, nueva_ubicacion:EUbicacion)->None:
        '''Esta funcion se encarga de actualizar la ubicacion de la 
        Estacion Espacial'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(nueva_ubicacion, EUbicacion):
            raise TypeError("nueva_ubicacion debe estar en la lista de ubicaciones disponibles")

        self.__ubicacion = nueva_ubicacion    

    def transmitirMensaje(self, mensaje:str, clave:int)->None:
        '''Esta funcion se encarga de transmitir un mensaje, verificando
        previamente si la clave es correcta'''

        super().transmitirMensaje(mensaje, clave)
        print(f"Estacion Estelar {self._idCombate}: {mensaje}")

class NaveEstelar(Nave):
    '''Clase hija de la clase Nave que se encarga de modelar las naves
    estelares del Imperio Galactico. Esta hereda los atributos del padre 
    y añade los atributos de tripulacion, pasaje y clase'''

    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, tripulacion:int, pasaje:int, clase:EClaseNave):
        '''Comprobamos que el tipo de dato introducido es correcto'''

        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        if not isinstance(tripulacion, int):
            raise TypeError("tripulacion debe ser un numero entero")
        
        if not isinstance(pasaje, int):
            raise TypeError("pasaje debe ser un numero entero")
        
        if not isinstance(clase, EClaseNave):
            raise TypeError("clase tiene que pertenecer a la enumeracion referente a las clases de las naves estelares")
        
        self.__tripulacion = tripulacion
        self.__pasaje = pasaje
        self.__clase = clase

    def transmitirMensaje(self, mensaje:str, clave:int)->None:
        '''Esta funcion se encarga de transmitir un mensaje, verificando 
        previamente si la clave dada es correcta'''

        super().transmitirMensaje(mensaje, clave)
        print(f"Nave Estelar {self._idCombate}: {mensaje}")

    def obtenerClase(self)->EClaseNave:
        '''Esta funcion se encarga devolver la clase de la nave estelar'''
        return self.__clase

class CazaEstelar(Nave):
    '''Clase hija de la clase Nave que modelo los cazas estelares del 
    Imperio Galactico. Esta, ademas de heredar los atributos del padre, 
    posee el atributo de dotacion'''

    def __init__(self, idCombate, claveCifrada, nombre, catalogoPiezas, dotacion:int):
        super().__init__(idCombate, claveCifrada, nombre, catalogoPiezas)
        '''Comprobamos que el tipo de dato introducido es correcto'''

        self.__dotacion = dotacion

        if not isinstance(dotacion, int):
            raise TypeError("dotacion TIENE QUE SER int")
        
        if dotacion < 0:
            raise ValueError("dotacion debe ser positivo o 0")

    def transmitirMensaje(self, mensaje:str, clave:int)->None:
        '''Esta funcion se encarga de transmitir un mensaje, verificando
        previamente si la clave es correcta'''

        super().transmitirMensaje(mensaje, clave)
        print(f"Caza Estelar {self._idCombate}: {mensaje}")

    def desplegarPiloto(self)->None:
        '''Esta funcion se encarga de desplegar a un piloto en un caza'''
        if self.__dotacion == 0:
            print("No se puede desplegar ningun piloto")
        else:
            print(f"Piloto desplegado\nQuedan {self.__dotacion - 1} pilotos por desplegar")

class Usuario(metaclass=ABCMeta):
    '''Clase abstracta que se encarga de modelar a los usuarios del sistema
    del Imperio Galactico'''

    def __init__(self, idUsuario:str, nombre:str):
        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(idUsuario, str):
            raise TypeError("idUsuario debe ser una cadena de texto")
        
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        self._idUsuario = idUsuario
        self._nombre = nombre

    @abstractmethod
    def iniciarSesion(self)->None:
        '''Metodo abstracto que se encarga de iniciar sesion en el sistema
        a un usuario. Como es un metodo abstracto, esta funcion se ejecutara
        en los hijos'''
        pass
    
    @abstractmethod
    def cerrarSesion(self)->None:
        '''Metodo abstracto que se encarga de cerrar sesion en el sistema
        a un usuario. Como es un metodo abstracto, esta funcion se ejecutara
        en los hijos'''
        pass

class Almacen:
    '''Clase que se encarga de modelar los almacenes del Imperio Galactico.
    Esta clase posee los atributos referentes al nombre y ubicacion del 
    almacen, asi como el catalogo de repuestos disponibles'''

    def __init__(self, nombre:str, ubicacion:str, catalogoRepuestos:list[Repuesto]):
        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        if not isinstance(ubicacion, str):
            raise TypeError("ubicacion debe ser una cadena de texto")
        
        if not all(isinstance(r, Repuesto) for r in catalogoRepuestos):
                    raise TypeError("El catálogo solo debe contener objetos Repuesto")
        
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.__catalogoRepuestos = catalogoRepuestos

    def añadirRepuesto(self, repuesto:Repuesto)->None:
        '''Esta funcion se encarga de añadir un repuesto a la lista de 
        repuestos disponibles'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto debe ser un objeto perteneciente a la clase Repuesto")
        
        self.__catalogoRepuestos.append(repuesto)

    def eliminarRepuesto(self, repuesto:str)->None:
        '''Esta funcion se encarga de eliminar un repuesto de la lista de
        repuestos disponibles'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, str):
            raise TypeError("repuesto debe ser una cadena de texto")
        
        for i in self.__catalogoRepuestos:
            if i.nombre == repuesto:
                return self.__catalogoRepuestos.remove(i)

        print(f"{repuesto} NO se encuentra en la lista de repuestos")

    def buscarRepuesto(self, repuesto:str)->bool:
        '''Esta funcion se encarga de buscar en la lista de repuestos
        un repuesto en concreto, devolviendo True se se encuentra'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, str):
            raise TypeError("repuesto debe ser una cadena de texto")
        
        for i in self.__catalogoRepuestos:
            if i.nombre == repuesto:
                return True
        return False
    
    def consultarStock(self, repuesto:Repuesto)->None:
        '''Esta funcion se encarga de mostrar toda la informacion de los
        repuestos en stock'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE PERTENECER A Repuesto")
        
        if len(self.__catalogoRepuestos) == 0:
            raise StockError("El stock del almacen esta vacio")
        
        for i in self.__catalogoRepuestos:
            print(f"Nombre: {i.nombre}\tProveedor: {i.proveedor}\nPrecio: {i.precio}")

class Comandante(Usuario):
    '''Clase hija de la clase Usuario que modela a los comandantes del
    Imperio Galactico. Esta clase hereda los atributos del padre'''

    def __init__(self, idUsuario, nombre):
        '''Comprobamos que el tipo de dato introducido es correcto'''

        super().__init__(idUsuario, nombre)
        
        self._repuestosSolicitados = {}

    def iniciarSesion(self)->str:
        '''Esta funcion se encarga de iniciar sesion a los comandantes del
        Imperio Galactico'''

        super().iniciarSesion()
        print(f"Comandante {self._nombre} con id {self._idUsuario} ha iniciado sesion")

    def cerrarSesion(self)->str:
        '''Esta funcion se encarga de cerrar sesion a los comandantes del 
        Imperio Galactico'''

        super().cerrarSesion()
        print(f"Comandante {self._nombre} con id {self._idUsuario} ha cerrado sesion")

    def consultarRepuesto(self, repuesto:str, almacen:Almacen)->bool:
        '''Esta funcion se encarga de, dado un repuesto y un almacen, se 
        encarga de buscar si este se encuentra en el almacen'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, str):
            raise TypeError("repuesto tiene que ser una cadena de texto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen tiene que ser un objeto de la clase Almacen")
        
        if almacen.buscarRepuesto(repuesto):
            print(f"{repuesto} se encuentra en el almacen")
            return True
        
        print(f"{repuesto} no se encuentra en el almacen")
        return False

    def solicitarRepuesto(self, repuesto:Repuesto, almacen:Almacen, cantidad:int)->None:
        '''Esta funcion se encarga de realizar un pedido de varios repuestos'''
        
        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuestos tiene que ser un objeto de la clase Repuesto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen tiene que pertenecer a la clase Almacen")
        
        if not isinstance(cantidad, int):
            raise TypeError("cantidad tiene que ser un numero entero")
        
        if cantidad < 0:
            raise ValueError("cantidad debe ser mayor que 0")
        
        if self.consultarRepuesto(repuesto.nombre, almacen) == False:
            raise StockError(f"El repuesto solicitado NO se encuentra en stock")

        if repuesto.obtenerUnidades() < cantidad:
            raise ValueError("La cantidad pedida es mayor a la habida en almacen")
        
        self._repuestosSolicitados[repuesto.nombre] = cantidad
        print(f"{repuesto.nombre} añadido a la lista de repuestos solicitados")

    def realizarPedido(self, almacen:Almacen)->None:
        '''Esta funcion se encarga de realizar un pedido al almacen, tomando
        la lista de repuestos creada en la funcion solicitarRepuesto'''

        if len(self._repuestosSolicitados) == 0:
            raise EmptyError("La lista de repuestos solicitados esta vacia")
        
        '''Comprobamos que el tipo de dato introducido es correcto'''
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen tiene que ser un objeto de la clase Almacen")
        
        for i in self._repuestosSolicitados.keys():
            if not self.consultarRepuesto(i, almacen):
                raise StockError(f"{i} NO se encuentra ya en stock")
            
        for k, v in self._repuestosSolicitados.items():
            almacen.eliminarRepuesto(k)

        self._repuestosSolicitados = {}
            
        print("Su pedido se ha realizado con exito") 

class OperarioAlmacen(Usuario):
    '''Clase hija de Usuario que se encarga de modelar a los operarios de
    almacen del Imperio Galactico. Esta clase hereda los atributos del padre'''

    '''Comprobamos que el tipo de dato introducido es correcto'''

    def __init__(self, idUsuario, nombre):
        super().__init__(idUsuario, nombre)

    def iniciarSesion(self)->None:
        '''Esta funcio se encarga de iniciar sesion a los operarios de 
        almacen del Imperio Galactico'''

        super().iniciarSesion()
        print(f"Operario de Almacen {self._nombre} con id {self._idUsuario} ha iniciado sesion")

    def cerrarSesion(self)->None:
        '''Esta funcio se encarga de cerrar sesion a los operarios de 
        almacen del Imperio Galactico'''

        super().cerrarSesion()
        print(f"Operario de Almacen {self._nombre} con id {self._idUsuario} ha cerrado sesion")

    def añadirRepuesto(self, repuesto:Repuesto, almacen:Almacen)->None:
        '''Esta funcion se encarga de añadir un repuesto a la lista de 
        repuestos del almacen'''

        '''Comprobamos que el tipo de dato introducido es correcto'''

        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto debe ser un objeto de la clase Repuesto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen debe ser un objeto de la clase Almacen")
        
        if almacen.buscarRepuesto(repuesto.nombre):
            print(f"{repuesto.nombre} ya se encuentra en el almacen")
        else:
            almacen.añadirRepuesto(repuesto)

    def eliminarRepuesto(self, repuesto:Repuesto, almacen:Almacen)->None:
        '''Esta funcio se encarga de, dado un repuesto y un almacen, 
        elimina el repuesto del catalogo de repuestos'''

        '''Comprobamos que el tipo de dato introducido es correcto'''
        
        if not isinstance(repuesto, Repuesto):
            raise TypeError("repuesto TIENE QUE PERTENECER A Repuesto")
        
        if not isinstance(almacen, Almacen):
            raise TypeError("almacen TIENE QUE PERTENECER A Almacen")

        if not almacen.buscarRepuesto(repuesto.nombre):
            print(f"{repuesto.nombre} NO se encuentra en el almacen")
        else:
            almacen.eliminarRepuesto(repuesto.nombre) 

'''Codigo para comprobar el buen funcionamiento del codigo'''
if __name__ == "__main__":

    '''Creacion de 2 objetos de la clase Repuesto'''
    motor = Repuesto("Motor", "Amazon", 10, 15000.0)
    turbina = Repuesto("Turbina", "Carrefour", 5, 2000.50)

    '''Creacion de dos objetos, uno del tipo almacen y el otro del tipo operario'''
    almacen = Almacen("Almacén", "Almacen A", [motor])
    operario = OperarioAlmacen("12345", "Pablo Guerra")

    operario.iniciarSesion()
    # El operario añade un repuesto nuevo
    operario.añadirRepuesto(turbina, almacen)
    operario.cerrarSesion()
    print("")

    '''Creamos 2 objetos, uno de la clase EstacionEspacial y otro de la clase CazaEstelar'''
    # El catálogo de la Estación incluye el motor
    UPCT = EstacionEspacial("24680", 1234, "UPCT", 
                                  ["Motor", "Turbina"], 
                                  50000, 100000, EUbicacion.ENDOR)
    
    UMA = CazaEstelar("13579", 9999, "UMA", ["Motor"], 1)

    # Probamos la transmision del mensaje
    try:
        UMA.transmitirMensaje("Atacando naves", 9999) # Clave correcta
        UPCT.transmitirMensaje("Sistemas operativos", 0000)     # Clave incorrecta
    except AccesoDenegado as e:
        print(f"Bloqueo de seguridad: {e}")
    print("")

    '''Creamos un objeto de la clase Comandante'''
    sara = Comandante("12457", "Sara")
    sara.iniciarSesion()

    # El comandante solicita piezas al almacén
    sara.solicitarRepuesto(motor, almacen, 2)
    sara.solicitarRepuesto(turbina, almacen, 1)

    # Realiza el pedido final
    sara.realizarPedido(almacen)
    
    # Verifica el stock que queda tras el pedido
    print(f"\nStock restante de motores: {motor.obtenerUnidades()} unidades.")
    sara.cerrarSesion()

