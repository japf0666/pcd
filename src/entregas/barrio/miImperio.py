from abc import ABCMeta, abstractmethod

# He creado estas clases para agrupar las opciones fijas de ubicación y clase. 
# Python no tiene enumeraciones asi que se ponen como constantes.
class Ubicacion:
    ENDOR = "Endor"
    CUMULO = "Cúmulo Raimos"
    NEBULOSA = "Nebulosa Kaliida"

class ClaseNave:
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"


# He separado Combate y Vehículo para poder hacer herencia multiple en Nave,
# ya que no todas los objetos de nave necesitan tener un nombre (Vehículo), 
# pero todas deben tener un id_combate y clave (Combate).

class Combate:
    def __init__(self, id_combate, clave):
        if type(id_combate) is not str:  # Comprobacion de tipo para id_combate
            raise TypeError("El ID de combate debe ser texto.")
        if type(clave) is not int:  # Comprobacion de tipo para clave
            raise TypeError("La clave debe ser un número entero.")
        self.id_combate = id_combate
        self.clave = clave

class Vehiculo:
    def __init__(self, nombre):
        if type(nombre) is not str: # Comprobacion de tipo para nombre
            raise TypeError("El nombre del vehículo debe ser texto.")
        if not nombre.strip(): # Comprobacion de que no este vacio
            raise ValueError("El nombre del vehículo no puede estar vacío.")
        self.nombre = nombre

# He definido Nave como clase abstracta porque no exixte ninguna nave pura sino que siempre es una estación espacial, nave estelar o caza estelar 
class Nave(Combate, Vehiculo, metaclass=ABCMeta):
    def __init__(self, id_combate, clave, nombre, catalogo):
        # Herencia multiple: Combate y Vehiculo.
        Combate.__init__(self, id_combate, clave)
        Vehiculo.__init__(self, nombre)
        if type(catalogo) is not list:
            raise TypeError("El catálogo debe ser una lista.")
        self.catalogo = catalogo

# Creo metodo para que funcione la libreria de las clases abstractas
    @abstractmethod
    def informacion(self):
        pass

# Estación Espacial hereda de Nave y le añado sus atributos.
class Estacion_Espacial(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        
        # Valido que los números sean enteros y no negativos.
        if type(tripulacion) is not int:
            raise TypeError("La tripulación debe ser entero.")
        if type(pasaje) is not int:
            raise TypeError("El pasaje debe ser entero.")
        if tripulacion < 0 or pasaje < 0:
            raise ValueError("La tripulación y el pasaje no pueden ser negativos.")
            
        # Aquí compruebo que la ubicación sea una de las que he definido en Ubicacion.
        opciones_validas = (Ubicacion.ENDOR, Ubicacion.CUMULO, Ubicacion.NEBULOSA)
        if ubicacion not in opciones_validas:
            raise ValueError(f"Ubicación incorrecta. Debe ser una de: {opciones_validas}")
            
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def informacion(self):
        print(f"Estación Espacial: {self.nombre}")

class Nave_Estelar(Nave):
    # Hereda de Nave y le añado sus atributos específicos.
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, clase):
        super().__init__(id_combate, clave, nombre, catalogo)
        
        if type(tripulacion) is not int:
            raise TypeError("La tripulación debe ser un número entero.")
        if type(pasaje) is not int:
            raise TypeError("El pasaje debe ser un número entero.")
        if tripulacion < 0 or pasaje < 0:
            raise ValueError("La tripulación y el pasaje no pueden ser negativos.")
            
        # Valido que la clase de nave sea una de las tres que hay en ClaseNave.
        opciones_validas = (ClaseNave.EJECUTOR, ClaseNave.ECLIPSE, ClaseNave.SOBERANO)
        if clase not in opciones_validas:
            raise ValueError(f"Clase de nave incorrecta. Debe ser una de: {opciones_validas}")
            
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def informacion(self):
        print(f"Nave Estelar de clase: {self.clase}")

class Caza_Estelar(Nave):
    # Hereda de Nave y le añado sus atributos.
    def __init__(self, id_combate, clave, nombre, catalogo, dotacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        
        if type(dotacion) is not int:
            raise TypeError("La dotación debe ser un número entero.")
        if dotacion < 0:
            raise ValueError("La dotación no puede ser negativa.")
        self.dotacion = dotacion

    def informacion(self):
        print(f"Caza Estelar: {self.nombre}")


class Repuesto:
    def __init__(self, nombre, proveedor, cantidad, precio):
        # Compruebo que los números sean enteros y no negativos.
        if type(nombre) is not str or type(proveedor) is not str:
            raise TypeError("Nombre y proveedor deben ser texto.")
        if type(cantidad) is not int:
            raise TypeError("La cantidad debe ser un número entero.")
        if cantidad < 0:
            raise ValueError("La cantidad inicial no puede ser negativa.")
        if type(precio) is not float:
            raise TypeError("El precio debe ser un número float.")
            
        self.nombre = nombre
        self.proveedor = proveedor
        # He puesto 'cantidad' como privado (__cantidad) como pide el enunciado
        self.__cantidad = cantidad
        self.precio = precio

    # He creado este 'getter' para poder consultar la cantidad.
    def get_cantidad(self):
        return self.__cantidad

    # He creado este 'setter' para poder modificar la cantidad.
    def set_cantidad(self, cant):
        try:
            # Compruebo que la cantidad sea un número entero y no negativo.
            if type(cant) is not int:
                raise TypeError("La nueva cantidad debe ser un número entero.")
            if cant < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            self.__cantidad = cant
        except (TypeError, ValueError) as e:
            print(f"Error: {e}")

class Almacen:
    def __init__(self, nombre, localizacion):
        if type(nombre) is not str:
            raise TypeError("El nombre del almacén debe ser texto.")
        self.nombre = nombre
        self.localizacion = localizacion
        self.repuestos = [] # Aquí se guardan los repuestos que hay en el almacén.

    # Con este método añado repuestos con el tipo correcto.
    def añadir_repuesto(self, repuesto):
        try:
            if type(repuesto) is not Repuesto:
                raise TypeError("Solo se pueden añadir repuestos.")
            self.repuestos.append(repuesto)
        except TypeError as e:
            print(f"Error: {e}")


# Usuario es una clase abstracta porque cada usuario tiene que ser o Comandante u Operario.
class Usuario(metaclass=ABCMeta):
    def __init__(self, nombre):
        # Compruebo que el nombre sea texto y no vacío.
        if type(nombre) is not str:
            raise TypeError("El nombre del usuario debe ser texto.")
        if not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self.nombre = nombre

# Metodo abstracto para que funcione la libreria de clases abstractas y para que cada usuario tenga su rol definido.
    @abstractmethod
    def rol(self):
        pass

class Comandante(Usuario):
    def rol(self):
        print(f"Rol: Comandante ({self.nombre})")

    # Este método permite ver que hay en los almacenes. 
    def consultar_repuesto(self, almacen):
        print(f"Catálogo: {almacen.nombre}")
        for r in almacen.repuestos:
            print(f"{r.nombre} (Quedan: {r.get_cantidad()})")

    # Con este metodo el comandante puede adquirir repuestos, siempre que haya stock.
    def adquirir_repuesto(self, almacen, nombre_rep):
        print(f"Comandante {self.nombre} quiere: {nombre_rep}")
        try:
            if type(almacen) is not Almacen:
                raise TypeError("No es un almacen.")
            if type(nombre_rep) is not str:
                raise TypeError("El nombre del repuesto a buscar debe ser texto.")

            encontrado = False
            for r in almacen.repuestos:
                if r.nombre == nombre_rep:
                    encontrado = True
                    if r.get_cantidad() > 0:
                        r.set_cantidad(r.get_cantidad() - 1)
                        print("Adquirido con éxito.")
                    else:
                        raise ValueError(f"No hay stock de {nombre_rep}")
            
            if not encontrado:
                raise ValueError(f"El repuesto {nombre_rep} no esta en el almacén.")
            
        except TypeError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

class Operario(Usuario):
    def rol(self):
        print(f"Rol: Operario ({self.nombre})")

    # Metodo para que el operario pueda mantener el stock de los repuestos, modificando su cantidad.
    def mantener_stock(self, repuesto, cantidad):
        print(f"Operario {self.nombre} ha actualizado el stock de {repuesto.nombre} a {cantidad}.")
        repuesto.set_cantidad(cantidad)



# Esta clase controla todo el Imperio.
class Miimperio:
    def __init__(self):
        self.almacenes = []
        self.usuarios = []
        self.naves = []

    # Metodos para llenar las listas.
    def añadir_almacen(self, almacen):
        if type(almacen) is not Almacen:
            raise TypeError("No es un almacen.")
        self.almacenes.append(almacen)

    def añadir_usuario(self, usuario):
        if type(usuario) is not Usuario and type(usuario) not in (Comandante, Operario):
            raise TypeError("No es un usuario válido.")
        self.usuarios.append(usuario)

    def añadir_nave(self, nave):
        if type(nave) not in (Estacion_Espacial, Nave_Estelar, Caza_Estelar):
            raise TypeError("No es un objeto Nave.")
        self.naves.append(nave)

    # Codigo de prueba
    def Pruebas(self):
        try:
            # Prueba de error de tipo en Repuesto.
            rep_error = Repuesto("Tornillo", "Pedro", "cinco", 10.5)
        except (TypeError, ValueError) as e:
            print(f"Prueba 1 (Error de tipo): {e}")

        try:
            # Intento crear un Usuario abstracto.
            usuario_error = Usuario("Usuario")
        except TypeError as e:
            print(f"Prueba 2 (Bloqueo clase abstracta): {e}")
            
        try:
            # Ubicación no válida.
            nave_error = Estacion_Espacial("0987", 1234, "EEI", ["Tornillo"], 100, 10, "Marte")
        except ValueError as e:
            print(f"Prueba 3 (Error enumeración): {e}")

        # Creacion correcta.
        almacen_endor = Almacen("Base A", "Endor")
        motor = Repuesto("Motor", "Pedro", 1, 500.0)
        almacen_endor.añadir_repuesto(motor)
        self.añadir_almacen(almacen_endor)
        
        Paco = Comandante("Paco")
        Paco.rol()
        self.añadir_usuario(Paco)
        
        # Comandante adquiriendo piezas.
        Paco.adquirir_repuesto(self.almacenes[0], "Motor") 
        Paco.adquirir_repuesto(self.almacenes[0], "Motor") 
        Paco.adquirir_repuesto(self.almacenes[0], "Láser") 

if __name__ == "__main__":
    milmperio = Miimperio()
    milmperio.Pruebas()