from enum import Enum
from abc import ABC, abstractmethod

# COMENZAMOS DEFINIENDO LAS EXPCECPIONES:
class ErrorRepuestoNoEncontrado(Exception):
    '''A la hora de realizar compras, modificaciones o cualquier acción que trate con una pieza, esta debe de existir'''
    pass

class ErrorStockInsuficiente(Exception):
    '''En el momento de realizar acciones como comprar o consultar una pieza, esta debe de tener el stock necesario para dicha acción. '''
    pass


class EUbicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3

class EClase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3


class UnidadesCombateEstelares(ABC):
    '''    
    Implementamos como clase abstracta, pues la unidad de 
    combate no es una 
    nave o vehículo concreto, sino un concepto general que 
    representa un elemento de la flota.
    '''
    
    def __init__(self, id_combate: str, clave: int):
        self.id_combate = id_combate
        self.__clave = clave

    def get_clave(self):
        return self.__clave
    
    @abstractmethod 
    def mostrar_especificaciones(self):
        pass # no devuelve nada, simplemente obliga a que las clases nietos tengan esta función.

class Nave(UnidadesCombateEstelares):
    '''
    Decidimos no ponerle el método asbtracto, pues realmente
    este objeto Nave, no representa una nave concreta, sino un 
    concepto de las características básicas que debe de tener 
    una nave.
    Así pues, debido a la herencia, esta tambíen será una clase asbtracta
    '''
    
    def __init__(self, id_combate: str, clave: int, nombre: str, piezas_repuesto: list):
        super().__init__(id_combate, clave)
        self.nombre = nombre
        self.piezas_repuesto = piezas_repuesto

class EstacionEspacial(Nave):
    
    def __init__(self, id_combate: str, clave: int, nombre: str, piezas_repuesto: list, tripulacion: int, pasaje: int, ubicacion: EUbicacion): 
        super().__init__(id_combate, clave, nombre, piezas_repuesto)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def mostrar_especificaciones(self):
        return f"Estación {self.nombre}, operando en {self.ubicacion.name}.A bordo {self.tripulacion} tripulantes y con capacidad para {self.pasaje} pasajeros."


class NaveEstelar(Nave):

    def __init__(self, id_combate: str, clave: int, nombre: str, piezas_repuesto: list, tripulacion: int, pasaje: int, clase: EClase):
        super().__init__(id_combate, clave, nombre, piezas_repuesto)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase
        
    def mostrar_especificaciones(self):
        return f"Nave estelar {self.nombre}, clase {self.clase.name}.A bordo {self.tripulacion} tripulantes y con capacidad para {self.pasaje} pasajeros."
    
class CazaEstelar(Nave):

    def __init__(self, id_combate: str, clave: int, nombre: str, piezas_repuesto: list, dotacion: int):
        super().__init__(id_combate, clave, nombre, piezas_repuesto)
        self.dotacion = dotacion

    
    def mostrar_especificaciones(self):
        return f"Caza {self.nombre}, con ID de comabte: {self.id_combate} . "
    
    
class Repuesto:
    def __init__(self, nombre_repuesto : str, proveedor : str,  cantidad_disponible : int, precio : float):
        self.nombre_repuesto = nombre_repuesto
        self.proveedor = proveedor
        self.__cantidad_disponible = cantidad_disponible
        self.precio = precio

    def get_nombre(self):
        return self.nombre_repuesto
    
    def get_precio(self): 
        return self.precio
    
    def get_cantidad_disponible(self): 
        return self.__cantidad_disponible
    
    def get_proveedor(self):
        return self.proveedor

    def set_cantidad_disponible(self, nueva_cantidad): 
        self.__cantidad_disponible = nueva_cantidad
    
    def __lt__(self, otro_repuesto): # método less than para poder comparar repuestos por precio
        return self.get_precio() < otro_repuesto.get_precio()
        
        
class Almacen:
    def __init__(self, nombre : str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo_repuestos = []
        
class UsuarioSistema(ABC):
    '''
    UsuariosSistema será una clase abstracta, porque no representa un ente concreto.
    Su funcionalidad es de clase base para determinar los atributos mínimos necesarios para poder estar en el sistema.
    '''
    
    def __init__(self, id_usuario : str, clave_usuario : int):
        self.id_usuario = id_usuario
        self.__clave_usuario = clave_usuario
    
    @abstractmethod 
    def mostrar_informacion(self):
        pass # no devuelve nada, simplemente obliga a que las clases hijas tengan esta función.

class Comandante(UsuarioSistema):
    ''' 
    En nuestro gestor de mantenimiento de la flota, el Comandante será el encargado de gestionar su nave, por tanto él será el único 
    que conozca las piezas que necesita así pues, surge la necesidad de poder conocer el precio, stock disponible de un repuesto 
    concreto, así como la posibilidad de comprar dicho repuesto. El Comandante a la hora de adqurir una pieza, no se preocupa del 
    almacen en el que se encuentra la pieza, simplemente si la pieza está o no, sin importar donde se encuentre.
    
    Así por tanto, una vez tenga la pieza adquirida esta se adjuntará a su propia nave, puede que se instale o simplemente esté a modo de reserva.
    '''
    def __init__(self, id_usuario : str, clave_usuario : int, nave_asignada : str):

        super().__init__(id_usuario, clave_usuario)
        
        self.nave_asignada = nave_asignada
    
    
    def mostrar_informacion(self):
        return f"Comandante {self.id_usuario} encargado de {self.nave_asignada.nombre}"

    
    def consultar_disponibilidad(self, nombre_pieza : str, almacenes_imperio : list): 
        ''' Buscamos la pieza entre los distintos catálogos de cada uno de los almacenes del Imperio Galáctico y devolvemos si la pieza se encuentra disponible.'''
        pieza_existe = False
        pieza_con_stock = False
        
        for almacen in almacenes_imperio:
            for repuesto in almacen.catalogo_repuestos:
                if repuesto.get_nombre() == nombre_pieza :
                    pieza_existe = True 
                    
                    if repuesto.get_cantidad_disponible() > 0:
                        pieza_con_stock = True
                        return True 
        
        if not pieza_existe:
            raise ErrorRepuestoNoEncontrado(f"Fallo en la consulta: El repuesto '{nombre_pieza}' no existe en la base de datos del Imperio.")
            
        else :
             raise ErrorStockInsuficiente(f"Fallo en la consulta: No hay stock disponible del repuesto '{nombre_pieza}'.")
   
    
    def consultar_precio(self, nombre_pieza : str, almacenes_imperio : list ):
        ''' Para una pieza concreta, buscamos el precio que tiene y además, se devuelve la pieza con menor precio entre todas ellas.'''  
        precio_mas_bajo = float('inf')
        pieza_existe = False
        pieza_con_stock = False
        repuesto_mas_barato = None

        for almacen in almacenes_imperio:
            for repuesto in almacen.catalogo_repuestos:
                if repuesto.get_nombre() == nombre_pieza :
                    pieza_existe = True # para las excpeciones usamos dos if, así detecatamos mejor donde se encuentra el error, si por stock o por inexistencia de pieza
                    
                    if repuesto.get_cantidad_disponible() > 0:
                        pieza_con_stock = True
                        if repuesto.get_precio() < precio_mas_bajo:
                            precio_mas_bajo = repuesto.get_precio()
                            repuesto_mas_barato = repuesto.get_nombre()
        
        if not pieza_existe:
            raise ErrorRepuestoNoEncontrado(f"Fallo en la consulta: El repuesto '{nombre_pieza}' no existe en la base de datos del Imperio.")
            
        if not pieza_con_stock:
             raise ErrorStockInsuficiente(f"Fallo en la consulta: No hay stock disponible del repuesto '{nombre_pieza}'.")

        return f"Mejor precio {precio_mas_bajo}, para el repuesto {repuesto_mas_barato}"
                
    def adquirir_repuesto(self, nombre_pieza : str, almacenes_imperio : list , cantidad : int ):
        '''Adquiere el número de repuestos necesarios en ese momento para una nave, actualiza el stock y además hace una consulta eficiente, quedándose con los repuestos más baratos.'''
        repuestos_mas_baratos = []
        stock_total = 0

        for almacen in almacenes_imperio:
            for repuesto in almacen.catalogo_repuestos:
                if repuesto.get_nombre() == nombre_pieza and (repuesto.get_cantidad_disponible()) > 0:
                    repuestos_mas_baratos.append(repuesto)
                    stock_total += repuesto.get_cantidad_disponible()
        
        if len(repuestos_mas_baratos) == 0:
            raise ErrorRepuestoNoEncontrado(f"Fallo en la compra: El repuesto '{nombre_pieza}' no existe en la base de datos del Imperio.")
        
        if stock_total < cantidad:
            raise ErrorStockInsuficiente(f"Fallo en la compra: No hay stock disponible del repuesto '{nombre_pieza}'.")
        
        repuestos_mas_baratos.sort() # ordenamos los repuestos que hemos insertado en la lista por precio de menor a mayor (funciona gracias al método lt)
        # recorremos la lista ordenada por precio en orden ascendente
        for repuesto in repuestos_mas_baratos: 
            while cantidad > 0 and repuesto.get_cantidad_disponible() > 0:
                nuevo_stock = repuesto.get_cantidad_disponible() - 1 #  recordamos que ahora la selección se hace de uno en uno
                repuesto.set_cantidad_disponible(nuevo_stock)

                self.nave_asignada.piezas_repuesto.append(nombre_pieza)
                cantidad = cantidad - 1
        return True
                    
class Operario(UsuarioSistema):
    '''
    En nuestro software gestor contratado por el Imperio Galáctico, la función de los operarios será el mantenimiento de los 
    almacenes que se encuentran por la galaxia. Un operario está ligado a un almacen y su objetivo será dada una entrada de repuestos 
    que le lleguen 'ordenarlos' en el catálogo del almacen. No obstante, también se pueden dar otras situaciones como que llegue un 
    nuevo modelo de un repuesto y el operario decida descatalogar el modelo antiguo. O una entrada masiva de un repuesto muy popular y tener que hacer 
    una modificación grande del stock.
    
    Tambíen, los operarios están muy concienciados con los tiempos de espera (que en el sistema gestor no se aprecian), así por tanto, si un repuesto es muy popular en las cercanias de un almacén concreto, 
    los operadores que trabajan allí, querrán tener el máximo stock posible del repuesto, para poder entregarlos de manera dinámica. 
    Cuando el proveedor no puede abastecer dicha demanda y en almacenes lejanos el producto no es tan popular, lo mejor para la correcta gestión del Imperio Galáctico, será poder abastecer el almacén popular.
    Por tanto surge la necesidad, de poder transferir repuestos entre almacenes.
    
    El operario a la hora de identificar un Repuesto, no puede hacerlo unícamente por el nombre, pues el mismo repuesto puede venir de diferentes proveedores y con distinto precio.
    Por tanto, hemos decidido que lo mejor será identificar un repuesto concreto por la tupla: nombre, proveedor. Esta consideración, no es tomada para comandnate, ya que ellos
    no están relacionados con los técnicismos que puede dar un repuesto según el proveedor.
    '''
    
    def __init__(self, id_usuario : str, clave_usuario : int, almacen_asignado : str):
        super().__init__(id_usuario, clave_usuario)
        
        self.almacen_asignado = almacen_asignado
    
    def mostrar_informacion(self):
        return f"Operario {self.id_usuario}, trabajador del almacen: {self.almacen_asignado.nombre}"

            
    def añadir_repuesto(self, nuevo_repuesto : Repuesto) :
        ''' Se trata de añadir un nuevo repuesto, en el caso de que exista, se incrementa su stock.'''
        nombre_repuesto= nuevo_repuesto.get_nombre()
        proveedor= nuevo_repuesto.get_proveedor()
        
        for pieza in self.almacen_asignado.catalogo_repuestos:
            if nombre_repuesto == pieza.get_nombre() and proveedor == pieza.get_proveedor():
                nuevo_stock = pieza.get_cantidad_disponible() + nuevo_repuesto.get_cantidad_disponible()
                pieza.set_cantidad_disponible(nuevo_stock)
                return True
        self.almacen_asignado.catalogo_repuestos.append(nuevo_repuesto)
        return True
        
    def eliminar_repuesto(self, nombre_repuesto : str, proveedor  : str):
        '''Eliminamos repuesto, dado su identificador'''
        for repuesto in self.almacen_asignado.catalogo_repuestos:
            if nombre_repuesto == repuesto.get_nombre() and proveedor == repuesto.get_proveedor():
                self.almacen_asignado.catalogo_repuestos.remove(repuesto)
                return True # la operación ha sido realizada con éxito
        raise ErrorRepuestoNoEncontrado(f"Fallo en la operación de eliminar: El repuesto '{nombre_repuesto}' no existe en la base de datos del Imperio.")

        
    def modificar_stock(self, nombre_repuesto : str, proveedor  : str, nueva_cantidad : int):
        '''Dado un repuesto modificamos el stock, para no tener que ir incrementando o decrementando de 1 en 1.'''
        for repuesto in self.almacen_asignado.catalogo_repuestos:
            if nombre_repuesto == repuesto.get_nombre() and proveedor == repuesto.get_proveedor():
                repuesto.set_cantidad_disponible(nueva_cantidad) 
                return True
        raise ErrorRepuestoNoEncontrado(f"Fallo en la operación de modificar: El repuesto '{nombre_repuesto}' no existe en la base de datos del Imperio.")
    
    
    def transferir_repuesto(self, almacen_destino, nombre_repuesto: str, proveedor  : str) :
        """Mueve un repuesto entero desde el almacén actual a otro almacén del Imperio."""
        for repuesto in self.almacen_asignado.catalogo_repuestos:
            if nombre_repuesto == repuesto.get_nombre() and proveedor == repuesto.get_proveedor():
                # Añadimos al almacén destino y eliminamos del actual
                almacen_destino.catalogo_repuestos.append(repuesto)
                self.almacen_asignado.catalogo_repuestos.remove(repuesto)
                return True
        raise ErrorRepuestoNoEncontrado(f"Fallo en la operación de eliminar: El repuesto '{nombre_repuesto}' no existe en la base de datos del Imperio.")
    

if __name__ == '__main__':  
    # Como el poryecto nos ha parecido muy entrentenido y ambos somos grandes fan de la saga Star Wars, hemos decidio 'dar algo de ambientación' a nuestro 
    # código de prueba
    import time 

    print("\n" + "-"*80)
    print("TERMINAL DE LOGÍSTICA DEL IMPERIO GALÁCTICO")
    print("Nivel de Acceso: ALTO MANDO | Encriptación: ACTIVA | Autenticación: OK ")
    print("-"*80)

    # --- ACTO 1: DESPLIEGUE DE LA FLOTA Y MANDOS ---
    print("\n[FASE 1: Inicializando Activos de la Flota...]")
    caza_vader = CazaEstelar(id_combate="TIE-ADV-X1", clave=1138, nombre="TIE Advanced", piezas_repuesto=[], dotacion=1)
    destructor = NaveEstelar(id_combate="SD-EXE", clave=5555, nombre="Ejecutor", piezas_repuesto=[], tripulacion=38000, pasaje=0, clase=EClase.EJECUTOR)
    estacion = EstacionEspacial(id_combate="DS-1", clave=9999, nombre="Estrella de la Muerte", piezas_repuesto=[], tripulacion=342953, pasaje=843342, ubicacion=EUbicacion.ENDOR)

    print(f" -> {caza_vader.mostrar_especificaciones()}")
    print(f" -> {destructor.mostrar_especificaciones()}")
    print(f" -> {estacion.mostrar_especificaciones()}")

    vader = Comandante(id_usuario="Lord Vader", clave_usuario=1234, nave_asignada=caza_vader)
    tarkin = Comandante(id_usuario="Grand Moff Tarkin", clave_usuario=1111, nave_asignada=estacion)

    # --- ACTO 2: INFRAESTRUCTURA DE ALMACENES Y OPERARIOS ---
    print("\n[FASE 2: Conectando a la Red de Almacenes...]")
    almacen_kuat = Almacen(nombre="Astilleros Kuat", localizacion="Mundos del Núcleo")
    almacen_endor = Almacen(nombre="Base Escudo Endor", localizacion="Borde Exterior")
    almacen_lothal = Almacen(nombre="Depósito Lothal", localizacion="Territorios del Borde Exterior")
    
    almacenes_imperio = [almacen_kuat, almacen_endor, almacen_lothal]

    operario_tk421 = Operario(id_usuario="TK-421", clave_usuario=4210, almacen_asignado=almacen_kuat)
    operario_fn2187 = Operario(id_usuario="FN-2187", clave_usuario=2187, almacen_asignado=almacen_endor)
    
    print(f" -> {operario_tk421.mostrar_informacion()} [EN LÍNEA]")
    print(f" -> {operario_fn2187.mostrar_informacion()} [EN LÍNEA]")

    # --- ACTO 3: GESTIÓN MASIVA DE INVENTARIO ---
    print("\n[FASE 3: Recepción de Cargamento y Logística]")
    # Creamos un mercado variado para probar a fondo el algoritmo de ordenación por precio
    m1 = Repuesto("Panel Solar TIE", "Sienar Fleet Systems", 50, 1500) # Calidad media
    m2 = Repuesto("Panel Solar TIE", "Chatarreros de Jakku", 20, 500)   # Muy barato, mala calidad
    m3 = Repuesto("Panel Solar TIE", "Kuat Drive Yards", 10, 3000)      # Premiumnm
    laser = Repuesto("Láser Turboláser", "Sienar Fleet Systems", 5, 12000)

    operario_tk421.añadir_repuesto(m1)
    operario_tk421.añadir_repuesto(m2)
    operario_tk421.añadir_repuesto(laser)
    operario_fn2187.añadir_repuesto(m3)
    
    print(" -> Cargamento registrado con éxito en todos los sistemas.")

    print("\n[ALERTA]: ¡Sabotaje Rebelde detectado en Astilleros Kuat!")
    print(" -> Ajustando inventario de Paneles Solares TIE de Sienar...")
    operario_tk421.modificar_stock("Panel Solar TIE", "Sienar Fleet Systems", 5) # Pasamos de 50 a solo 5
    print(" -> Daños evaluados. Stock actualizado de 50 a 5 unidades.")

    # --- ACTO 4: TÁCTICAS DEL ALTO MANDO ---
    print("\n[FASE 4: Peticiones del Alto Mando]")
    print(f"[{tarkin.id_usuario}]: 'Verificando defensas de la estación...'")
    disponible = tarkin.consultar_disponibilidad("Láser Turboláser", almacenes_imperio)
    if disponible:
        print(" -> Sistema: Hay Láseres Turboláser disponibles en la red.")

    print(f"\n[{vader.id_usuario}]: 'Necesito 22 Paneles Solares TIE para mi escuadrón. Buscad el mejor precio.'")
    precio_optimo = vader.consultar_precio("Panel Solar TIE", almacenes_imperio)
    print(f" -> Sistema Informa: {precio_optimo}")

    print(f"[{vader.id_usuario}]: 'Procedan con la adquisición.'")
    # Vader necesita 22. El algoritmo debe coger: 20 de Jakku (los más baratos) + 2 de Sienar (los siguientes). Los de Kuat ni los toca.
    exito = vader.adquirir_repuesto("Panel Solar TIE", almacenes_imperio, cantidad=22)
    if exito:
        print(" -> Compra aprobada.")
        print(f" -> Inventario actual del caza de Vader: {vader.nave_asignada.piezas_repuesto}")
        
    print("\n[Auditoría de Stock tras la compra masiva de Lord Vader]:")
    print(f" - Stock Chatarreros de Jakku (Barato): {m2.get_cantidad_disponible()} unidades (Deberían quedar 0).")
    print(f" - Stock Sienar Fleet (Medio): {m1.get_cantidad_disponible()} unidades (Deberían quedar 3).")
    print(f" - Stock Kuat (Caro): {m3.get_cantidad_disponible()} unidades (Deberían quedar intactas las 10).")

    # --- ACTO 5: MANEJO DE EXCEPCIONES CRÍTICAS ---
    print("\n" + "!"*80)
    print("SIMULACRO DE ESTRÉS DEL SISTEMA (COMPROBANDO EXCEPCIONES)")
    print("!"*80)

    # Prueba 1: Eliminar un repuesto que no existe en el catálogo
    print("\n>> Prueba 1: Operario intenta purgar datos de un Motor hiperimpulsor inexistente...")
    try:
        operario_fn2187.eliminar_repuesto("Motor Hiperimpulsor", "Corellian Eng.")
    except ErrorRepuestoNoEncontrado as e:
        print(f" [EXCEPCIÓN CONTROLADA] -> {e}")

    # Prueba 2: Comprar algo sin stock suficiente
    print("\n>> Prueba 2: Tarkin exige 100 Láseres Turboláser (Solo quedan 5)...")
    try:
        tarkin.adquirir_repuesto("Láser Turboláser", almacenes_imperio, 100)
    except ErrorStockInsuficiente as e:
        print(f" [EXCEPCIÓN CONTROLADA] -> {e}")

    # Prueba 3: Consultar disponibilidad de un mito
    print("\n>> Prueba 3: Tarkin busca los planos de la Estrella de la Muerte robados...")
    try:
        tarkin.consultar_disponibilidad("Planos Estrella de la Muerte", almacenes_imperio)
    except ErrorRepuestoNoEncontrado as e:
        print(f" [EXCEPCIÓN CONTROLADA] -> {e}")

    print("\n" + "-"*80)
    print("SIMULACIÓN FINALIZADA - EL IMPERIO ES AHORA MÁS FUERTE.")
    print("-"*80 + "\n")