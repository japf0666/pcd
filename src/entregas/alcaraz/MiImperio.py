from abc import ABC, abstractmethod
from enum import Enum

# ==========================================
# --- ENUMERACIONES ---
# DECISIÓN DE DISEÑO: Utilizamos Enum para restringir los valores de ubicaciones y 
# clases de naves a un conjunto predefinido. Esto evita errores tipográficos en el código
# y asegura la coherencia de los datos en todo el sistema.
# ==========================================
class Ubicacion(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class ClaseNave(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"


# ==========================================
# --- CLASES DE IDENTIDAD ---
# ==========================================
# DECISIÓN DE DISEÑO: Usuario hereda de ABC (Abstract Base Class). 
# Nunca crearemos un "Usuario" genérico, siempre serán Comandantes u Operarios,
# por lo que esta clase sirve únicamente para heredar el atributo 'nombre'.
class Usuario(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

class Comandante(Usuario):
    # DECISIÓN DE DISEÑO: Delegación de responsabilidades. El Comandante no modifica
    # el almacén directamente, sino que le da la orden al objeto 'nave'.
    def comprar_repuesto(self, nave, almacen, pieza_nombre):
        print(f"\n[ORDEN] Comandante {self.nombre} solicita {pieza_nombre}.")
        try:
            # Intentamos ejecutar la acción en la nave
            nave.solicitar_repuesto(almacen, pieza_nombre)
        except AttributeError:
            # DECISIÓN DE SEGURIDAD: Programación defensiva. Capturamos AttributeError 
            # por si se pasa un objeto que no es una nave (ej. un string o int).
            print(f"[ERROR CRÍTICO] La orden ha fallado: El objeto '{nave}' no es una unidad de combate válida para esta acción.")

    def revisar_inventario(self, almacen):
        print(f"\n[CONSULTA] Comandante {self.nombre} revisando inventario.")
        almacen.mostrar_catalogo()

class OperarioAlmacen(Usuario):
    def agregar_repuesto(self, almacen, repuesto):
        
        almacen.agregar_repuesto(repuesto)
        print(f"[LOGÍSTICA] Repuesto {repuesto.nombre} añadido.")


# ==========================================
# --- BLOQUE DE COMBATE ---
# ==========================================
# DECISIÓN DE DISEÑO: UnidadCombate es abstracta. Define un contrato estricto
# obligando a todas sus subclases a implementar el método mostrar_info() a través 
# del decorador @abstractmethod, garantizando así el Polimorfismo.
class UnidadCombate(ABC):
    def __init__(self, identificador_combate: str, clave_cifrada: int):
        self.identificador_combate = identificador_combate
        self.clave_cifrada = clave_cifrada

    @abstractmethod
    def mostrar_info(self):
        pass

class Vehiculo_Terrestres(UnidadCombate):
    def __init__(self, id_c, clave, nombre):
        super().__init__(id_c, clave) # Llamada al constructor de la clase padre
        self.nombre = nombre
        self.catalogo_piezas = [] # List[str]

    def mostrar_info(self):
        # Implementación específica del polimorfismo para vehículos terrestres
        print(f"VEHÍCULO TERRESTRE: {self.nombre} | ID: {self.identificador_combate}")

    def consultar_repuestos(self, almacen):
        almacen.mostrar_catalogo()

    def solicitar_repuesto(self, almacen, pieza_str):
        # Primero delegamos en el almacén la búsqueda de la pieza
        pieza = almacen.buscar_repuesto(pieza_str)
        if pieza:
            try:
                # Si existe, intentamos retirarla. Si no hay stock, esto levantará un SinStockError
                pieza.retirar_stock()
                print(f"[ÉXITO] {pieza_str} obtenido para el vehículo {self.nombre}.")
            except Exception as e:
                # Capturamos el error de stock para evitar que el programa colapse
                print(f"[ERROR] {e}")
        else:
            print(f"[ERROR] {pieza_str} no existe en almacén.")

class Nave(UnidadCombate):
    def __init__(self, id_c, clave, nombre):
        super().__init__(id_c, clave)
        self.nombre = nombre
        self.catalogo_piezas = [] # List[str] 

    def mostrar_info(self):
        # Implementación específica del polimorfismo para Nave
        print(f"NAVE: {self.nombre} | ID: {self.identificador_combate}")

    def consultar_repuestos(self, almacen):
        almacen.mostrar_catalogo()
    
    def solicitar_repuesto(self, almacen, pieza_str):
        # Lógica idéntica a Vehículo Terrestre para mantener coherencia en la interfaz
        # 1. Llamamos al método del almacén para ver si el nombre de la pieza existe en su catálogo.
        # Guardamos el resultado (que será un objeto Repuesto o None) en la variable 'pieza'.
        pieza = almacen.buscar_repuesto(pieza_str)

        # 2. Comprobamos si la búsqueda tuvo éxito. Si 'pieza' no es None, entramos en el bloque.
        if pieza:
            # 3. Usamos un bloque try-except porque intentar sacar stock puede fallar (si hay 0 unidades).
            try:
                # 4. Ejecutamos el método del objeto Repuesto para reducir su cantidad en 1.
                # Si el stock es 0, este método 'lanzará' (raise) un SinStockError.
                pieza.retirar_stock()
                
                # 5. Si la línea anterior no dio error, confirmamos el éxito de la operación.
                print(f"[ÉXITO] {pieza_str} obtenido.")
            
            # 6. Si ocurrió cualquier error (como SinStockError), el programa no se detiene;
            # salta directamente aquí y guarda el mensaje del error en la variable 'e'.
            except Exception as e:
                # 7. Mostramos el mensaje específico del error (ej: "No hay stock de Motor").
                print(f"[ERROR] {e}")
        
        # 8. Si en el paso 2 la pieza ni siquiera existía en el catálogo del almacén:
        else:
            # 9. Informamos de que el nombre solicitado no coincide con nada en el inventario.
            print(f"[ERROR] {pieza_str} no existe en almacén.")

# --- SUBTIPOS DE NAVE (Polimorfismo y Herencia Multilnivel) ---
class EstacionEspacial(Nave):
    # 1. El método __init__ es el constructor. Recibe los datos genéricos (id_c, clave, nombre) 
    # y los específicos de la estación
    def __init__(self, id_c, clave, nombre, tripulacion: int, pasaje: int, ubicacion: Ubicacion):
        # 2. La función super() es una "llamada al padre" (la clase Nave). 
        # Le enviamos los datos básicos para que Nave se encargue de guardarlos.
        # De esta forma evitamos escribir self.nombre = nombre otra vez.
        super().__init__(id_c, clave, nombre)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def mostrar_info(self):
        # Usamos super().mostrar_info() para imprimir la info genérica de Nave, 
        # y luego le añadimos la info específica de EstacionEspacial.
        super().mostrar_info()
        print(f" > Estación en {self.ubicacion.value} | Personal: {self.tripulacion}")

class NaveEstelar(Nave):
    def __init__(self, id_c, clave, nombre, tripulacion: int, pasaje: int, clase: ClaseNave):
        super().__init__(id_c, clave, nombre)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def mostrar_info(self):
        # Usamos super().mostrar_info() para imprimir la info genérica de Nave, 
        # y luego le añadimos la info específica de NaveEstelar.
        super().mostrar_info()
        print(f" > Nave Clase {self.clase.value} | Pasaje: {self.pasaje}")

class CazaEstelar(Nave):
    def __init__(self, id_c, clave, nombre, dotacion: int):
        super().__init__(id_c, clave, nombre)
        self.dotacion = dotacion

    def mostrar_info(self):
        # Usamos super().mostrar_info() para imprimir la info genérica de Nave, 
        # y luego le añadimos la info específica de CazaEstelar.
        super().mostrar_info()
        print(f" > Caza Estelar | Dotación: {self.dotacion}")


# ==========================================
# --- LOGÍSTICA ---
# ==========================================
# DECISIÓN DE DISEÑO: En este bloque agrupamos la gestión del inventario físico.
# Hemos creado un error a medida llamado 'SinStockError'. La lógica de hacer esto
# es que, si un Comandante pide una pieza que ya se ha agotado, el programa nos 
# avise con un fallo claro y específico de nuestro sistema, en lugar de que Python 
# lance un error genérico (como ValueError) que sea confuso y difícil de rastrear.

class SinStockError(Exception):
    pass

class Repuesto:
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: float):
        # Prevenimos estados inconsistentes desde la creación
        if cantidad < 0 or precio < 0:
            raise ValueError(f"Error al registrar '{nombre}': La cantidad y el precio no pueden ser negativos.")
        self.nombre = nombre
        self.proveedor = proveedor
        
        # ENCAPSULAMIENTO: El doble guion bajo (__) hace que el atributo sea "privado" en Python.
        # Esto evita modificaciones externas y protege la integridad del stock.
        self.__cantidad = cantidad 
        self.precio = precio

    def agregar_stock(self, n: int): 
            # Validación para asegurar que no se ingrese stock negativo por error
            if n <= 0:
                raise ValueError("La cantidad a añadir debe ser mayor a cero.")
            self.__cantidad += n

    def retirar_stock(self): 
        # Única vía autorizada para reducir stock. Si llega a 0, lanza nuestra excepción.
        if self.__cantidad > 0:
            self.__cantidad -= 1
        else:
            raise SinStockError(f"No hay stock de {self.nombre}")

    def obtener_cantidad(self):
        # Esto sirve para consultar el stock protegido
        return self.__cantidad

class Almacen:
    def __init__(self, nombre: str, ubicacion: str):
        self.nombre = nombre
        self.ubicacion = ubicacion
        # RELACIÓN DE AGREGACIÓN: El Almacen "tiene" Repuestos. Si el Almacen desaparece,
        # conceptualmente los repuestos podrían seguir existiendo.
        self.catalogo = [] # Agregación 0..n

    def agregar_repuesto(self, repuesto: Repuesto): 
        # VALIDACIÓN: Garantizamos que solo objetos Repuesto entren en la lista,
        # evitando fallos futuros al iterar sobre el catálogo.
        if not isinstance(repuesto, Repuesto):
            raise TypeError("Solo se pueden añadir objetos de tipo 'Repuesto' al catálogo.")
        self.catalogo.append(repuesto)

    def buscar_repuesto(self, nombre_pieza: str): 
        for r in self.catalogo:
            if r.nombre == nombre_pieza:
                return r
        return None

    def mostrar_catalogo(self): 
        print(f"--- Almacén: {self.nombre} ---")
        for r in self.catalogo:
            print(f"Pieza: {r.nombre} | Stock: {r.obtener_cantidad()}")


# ==========================================
# --- PRUEBA EJECUTABLE (SIMULACIÓN PASO A PASO) ---
# ==========================================
if __name__ == "__main__":
    print("="*60)
    print("INICIO DE LA AUDITORÍA LOGÍSTICA DEL IMPERIO")
    print("="*60)

    # PASO 1: Creación de la Infraestructura
    # Explicación: Primero necesitamos dónde guardar las piezas y quién las gestione.
    print("\n[PASO 1]: Configurando almacenes y personal...")
    alm_endor = Almacen("Sector 7 (Endor)", Ubicacion.ENDOR.value)
    tarkin = OperarioAlmacen("Wilhuff Tarkin")
    
    # PASO 2: Abastecimiento (Probando Operario y Repuestos)
    # Explicación: El operario usa su método para llenar el almacén. 
    # Aquí probamos que la agregación de objetos Repuesto al Almacen funciona.
    print("\n[PASO 2]: El Operario Tarkin abastece el almacén...")
    rep_motor = Repuesto("Motor Iónico", "Sienar Fleet Systems", 1, 5000.0)
    rep_blindaje = Repuesto("Placa de Titanio", "Kuat Drive Yards", 2, 1200.0)
    
    tarkin.agregar_repuesto(alm_endor, rep_motor)
    tarkin.agregar_repuesto(alm_endor, rep_blindaje)

    # PASO 3: Despliegue de Unidades (Probando Polimorfismo)
    # Explicación: Creamos diferentes tipos de unidades para ver cómo cada una
    # responde al método mostrar_info() de forma distinta (Polimorfismo).
    print("\n[PASO 3]: Desplegando flota y unidades de tierra...")
    vader_caza = CazaEstelar("TIE-Adv", 101, "Caza de Darth Vader", 1)
    at_at = Vehiculo_Terrestres("AT-AT-05", 55, "Caminante Pesado")
    estrella = EstacionEspacial("DS-1", 1, "Estrella de la Muerte", 1000000, 50000, Ubicacion.ENDOR)

    lista_unidades = [vader_caza, at_at, estrella]
    for unidad in lista_unidades:
        unidad.mostrar_info()

    # PASO 4: Acciones del Comandante (Probando Interacción y Encapsulamiento)
    # Explicación: Un comandante revisa el stock y ordena reparaciones.
    # Aquí vemos cómo el stock baja de forma segura (encapsulamiento).
    print("\n[PASO 4]: El Comandante Darth Vader inicia el mantenimiento...")
    vader = Comandante("Darth Vader")
    vader.revisar_inventario(alm_endor)

    # Compra exitosa: El stock bajará de 1 a 0.
    vader.comprar_repuesto(vader_caza, alm_endor, "Motor Iónico")

    # PASO 5: Prueba de Errores y Robustez (Excepciones)
    # Explicación: Vamos a forzar fallos para demostrar que el código es estable.
    print("\n[PASO 5]: Pruebas de seguridad y gestión de errores...")

    # A) Intento de compra SIN STOCK (Debe saltar SinStockError)
    print("\n- Intento 1: Pedir una pieza agotada (Motor Iónico ya se usó)...")
    vader.comprar_repuesto(vader_caza, alm_endor, "Motor Iónico")

    # B) Intento de compra de pieza INEXISTENTE
    print("\n- Intento 2: Pedir una pieza que no está en el catálogo...")
    vader.comprar_repuesto(at_at, alm_endor, "Hipermotor Clase 1")

    # C) Prueba de validación de DATOS NEGATIVOS (ValueError)
    print("\n- Intento 3: Intentar crear un repuesto con precio negativo...")
    try:
        rep_error = Repuesto("Pieza Corrupta", "Contrabando", 10, -50.0)
    except ValueError as e:
        print(f"[CAPTURA CORRECTA]: {e}")

    # D) Prueba de ROBUSTEZ de tipos (TypeError)
    print("\n- Intento 4: Intentar meter un texto en el catálogo del almacén...")
    try:
        alm_endor.agregar_repuesto("Esto no es un objeto Repuesto")
    except TypeError as e:
        print(f"[CAPTURA CORRECTA]: {e}")

    # E) Prueba de FALLO DE OBJETO (AttributeError)
    print("\n- Intento 5: El comandante da una orden a un objeto que no puede procesarla...")
    vader.comprar_repuesto("Soy un texto, no una Nave", alm_endor, "Placa de Titanio")

    print("\n" + "="*60)
    print("AUDITORÍA FINALIZADA: TODOS LOS SISTEMAS OPERATIVOS")
    print("="*60)