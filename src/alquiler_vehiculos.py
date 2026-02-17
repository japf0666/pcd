# Agencia de Alquiler de Vehículos

class Vehiculo:
    def __init__(self, vehiculo_id, modelo, annio, tarifa_diaria):
        self.vehiculo_id = vehiculo_id
        self.modelo = modelo
        self.año = annio
        self.tarifa_diaria = tarifa_diaria
        self.disponible = True

    def __str__(self):
        return f"ID: {self.vehiculo_id}, \
                Modelo: {self.modelo},   \
                Año: {self.año},         \
                Tarifa Diaria: ${self.tarifa_diaria}, \
                Disponible: {'Sí' if self.disponible else 'No'}"
    
    def alquilar(self):
        if not self.disponible:
            print(f"El vehículo {self.vehiculo_id} ya está alquilado")
        self.disponible = False

    def devolver(self):
        if self.disponible:
            print(f"El vehículo {self.vehiculo_id} no está alquilado")
        self.disponible = True

    def calcular_costo(self, dias):
        return self.tarifa_diaria * dias

    
class Coche(Vehiculo):
    def __init__(self, vehiculo_id, modelo, annio, tarifa_diaria, num_puertas):
        super().__init__(vehiculo_id, modelo, annio, tarifa_diaria)
        self.num_puertas = num_puertas

    def __str__(self):
        return super().__str__() + f", Número de Puertas: {self.num_puertas}"
    
    
class Bicicleta(Vehiculo):
    def __init__(self, vehiculo_id, modelo, annio, tarifa_diaria, pinnones):
        super().__init__(vehiculo_id, modelo, annio, tarifa_diaria)
        self.pinnones = pinnones

    def __str__(self):
        return super().__str__() + f", Número de Piñones: {self.pinnones}"


class Cliente:
    def __init__(self, cliente_id, nombre, contacto):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.contacto = contacto

    def __str__(self):
        return f"ID: {self.cliente_id}, Nombre: {self.nombre}, Contacto: {self.contacto}"
    
class ContratoAlquiler:

    def __init__(self, cliente, vehiculo, fecha_comienzo, dias):
        self.id = f"{cliente.cliente_id}_{vehiculo.vehiculo_id}_{fecha_comienzo}"
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.fecha_comienzo = fecha_comienzo
        self.dias = dias
        self.costo_total = self.vehiculo.calcular_costo(dias)
        self.finalizado = False

    def __str__(self):
        return f"Contrato Alquiler, ID: {self.id}, \
                 Cliente: {self.cliente.nombre}, \
                 Vehículo: {self.vehiculo.modelo}, \
                 Fecha de Comienzo: {self.fecha_comienzo}, \
                 Días: {self.dias}, \
                 Finalizado: {'Sí' if self.finalizado else 'No'}, \
                 Costo Total: ${self.vehiculo.calcular_costo(self.dias)}"
    
    def finalizar_contrato(self):
        if self.finalizado:
            print("El contrato ya ha sido finalizado.")
            return
        self.vehiculo.devolver()
        self.finalizado = True
        print(f"Contrato finalizado. Costo total: ${self.costo_total}")

    def fecha_devolucion(self):
        from datetime import datetime, timedelta
        fecha_comienzo_dt = datetime.strptime(self.fecha_comienzo, "%Y-%m-%d")
        fecha_devolucion_dt = fecha_comienzo_dt + timedelta(days=self.dias)
        return fecha_devolucion_dt.strftime("%Y-%m-%d")


class AgenciaAlquiler:
    def __init__(self):
        self.vehiculos = []
        self.clientes = []
        self.contratos = []

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def alquilar_vehiculo(self, cliente_id, vehiculo_id, dias):
        cliente = next((c for c in self.clientes if c.cliente_id == cliente_id), None)
        vehiculo = next((v for v in self.vehiculos if v.vehiculo_id == vehiculo_id), None)

        if cliente and vehiculo and vehiculo.disponible:
            contrato = ContratoAlquiler(cliente, vehiculo, fecha_comienzo=date.today(), dias=dias)
            self.contratos.append(contrato)
            vehiculo.alquilar()
            print(f"Vehículo {vehiculo.modelo} alquilado a {cliente.nombre} por {dias} días.")
        else:
            print("No se pudo realizar el alquiler. Verifique el cliente, vehículo o disponibilidad.")

    def devolver_vehiculo(self, cliente_id, vehiculo_id):
        contrato = next((c for c in self.contratos if c.cliente.cliente_id == cliente_id and c.vehiculo.vehiculo_id == vehiculo_id), None)
        if contrato:
            contrato.finalizar_contrato()
        else:
            print("No se encontró un contrato para devolver el vehículo.")

    
    def buscar_vehiculo_por(self, criterio, primero=False):
        """Buscar vehículos usando un `criterio` callable.

        - `criterio` debe ser una función que reciba un `Vehiculo` y devuelva `True` si
          el vehículo cumple el criterio (p. ej. `lambda v: v.año >= 2020 and v.disponible`).
        - Si `primero` es True devuelve el primer `Vehiculo` que cumpla el criterio o
          `None` si no hay ninguno. Si `primero` es False, devuelve la lista de coincidencias.
        """
        if not callable(criterio):
            raise TypeError("criterio debe ser callable (p.ej. lambda v: ...)")
        if primero:
            for v in self.vehiculos:
                if criterio(v):
                    return v
            return None
        return [v for v in self.vehiculos if criterio(v)]


from datetime import datetime, date

class UIInterface:
    """Interfaz de usuario basada en consola para AgenciaAlquiler."""
    
    def __init__(self, agencia):
        """Inicializa la interfaz con una instancia de AgenciaAlquiler.
        
        Args:
            agencia: instancia de AgenciaAlquiler
        """
        if not isinstance(agencia, AgenciaAlquiler):
            raise TypeError("agencia debe ser una instancia de AgenciaAlquiler")
        self.agencia = agencia
    
    def mostrar_menu(self):
        """Muestra el menú principal."""
        print("\n" + "="*50)
        print("   AGENCIA DE ALQUILER DE VEHÍCULOS")
        print("="*50)
        print("1. Gestionar Vehículos")
        print("2. Gestionar Clientes")
        print("3. Alquilar Vehículo")
        print("4. Devolver Vehículo")
        print("5. Buscar Vehículo")
        print("6. Ver Todos los Vehículos")
        print("7. Ver Todos los Clientes")
        print("8. Ver Contratos Activos")
        print("0. Salir")
        print("="*50)
    
    def ejecutar(self):
        """Loop principal de la interfaz."""
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self._gestionar_vehiculos()
            elif opcion == "2":
                self._gestionar_clientes()
            elif opcion == "3":
                self._alquilar_vehiculo()
            elif opcion == "4":
                self._devolver_vehiculo()
            elif opcion == "5":
                self._buscar_vehiculo()
            elif opcion == "6":
                self._ver_vehiculos()
            elif opcion == "7":
                self._ver_clientes()
            elif opcion == "8":
                self._ver_contratos()
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
    
    def _gestionar_vehiculos(self):
        """Submenu para gestionar vehículos."""
        print("\n--- Gestionar Vehículos ---")
        print("1. Agregar Coche")
        print("2. Agregar Bicicleta")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()
        
        if opcion == "1":
            vid = input("ID Vehículo: ").strip()
            modelo = input("Modelo: ").strip()
            year = int(input("Año: "))
            tarifa = float(input("Tarifa Diaria: "))
            puertas = int(input("Número de Puertas: "))
            self.agencia.agregar_vehiculo(Coche(vid, modelo, year, tarifa, puertas))
            print(f"Coche '{modelo}' agregado correctamente.")
        elif opcion == "2":
            vid = input("ID Vehículo: ").strip()
            modelo = input("Modelo: ").strip()
            year = int(input("Año: "))
            tarifa = float(input("Tarifa Diaria: "))
            pinnones = int(input("Número de Piñones: "))
            self.agencia.agregar_vehiculo(Bicicleta(vid, modelo, year, tarifa, pinnones))
            print(f"Bicicleta '{modelo}' agregada correctamente.")
    
    def _gestionar_clientes(self):
        """Submenu para gestionar clientes."""
        print("\n--- Gestionar Clientes ---")
        cid = input("ID Cliente: ").strip()
        nombre = input("Nombre: ").strip()
        contacto = input("Contacto: ").strip()
        self.agencia.agregar_cliente(Cliente(cid, nombre, contacto))
        print(f"Cliente '{nombre}' agregado correctamente.")
    
    def _alquilar_vehiculo(self):
        """Alquilar un vehículo."""
        print("\n--- Alquilar Vehículo ---")
        cliente_id = input("ID Cliente: ").strip()
        vehiculo_id = input("ID Vehículo: ").strip()
        dias = int(input("Número de días: "))
        self.agencia.alquilar_vehiculo(cliente_id, vehiculo_id, dias=dias)
    
    def _devolver_vehiculo(self):
        """Devolver un vehículo."""
        print("\n--- Devolver Vehículo ---")
        cliente_id = input("ID Cliente: ").strip()
        vehiculo_id = input("ID Vehículo: ").strip()
        self.agencia.devolver_vehiculo(cliente_id, vehiculo_id)
    
    def _buscar_vehiculo(self):
        """Buscar vehículos por criterios."""
        print("\n--- Buscar Vehículo ---")
        print("1. Por modelo")
        print("2. Por disponibilidad")
        print("3. Por año mínimo")
        print("0. Volver")
        opcion = input("Seleccione: ").strip()
        
        if opcion == "1":
            modelo = input("Modelo (parcial): ").strip()
            resultados = self.agencia.buscar_vehiculo(modelo)
            self._mostrar_resultados(resultados)
        elif opcion == "2":
            disponible = input("¿Disponible? (s/n): ").lower().strip() == "s"
            resultados = self.agencia.buscar_vehiculo_por(lambda v: v.disponible == disponible)
            self._mostrar_resultados(resultados)
        elif opcion == "3":
            año_min = int(input("Año mínimo: "))
            resultados = self.agencia.buscar_vehiculo_por(lambda v: v.año >= año_min)
            self._mostrar_resultados(resultados)
    
    def _ver_vehiculos(self):
        """Ver todos los vehículos."""
        print("\n--- Vehículos Disponibles ---")
        if not self.agencia.vehiculos:
            print("No hay vehículos registrados.")
        else:
            for v in self.agencia.vehiculos:
                print(f"  {v}")
    
    def _ver_clientes(self):
        """Ver todos los clientes."""
        print("\n--- Clientes Registrados ---")
        if not self.agencia.clientes:
            print("No hay clientes registrados.")
        else:
            for c in self.agencia.clientes:
                print(f"  {c}")
    
    def _ver_contratos(self):
        """Ver contratos activos."""
        print("\n--- Contratos Activos ---")
        contratos_activos = [c for c in self.agencia.contratos if not c.finalizado]
        if not contratos_activos:
            print("No hay contratos activos.")
        else:
            for c in contratos_activos:
                print(f"  {c}")
    
    def _mostrar_resultados(self, resultados):
        """Muestra resultados de búsqueda."""
        if not resultados:
            print("No se encontraron vehículos con los criterios especificados.")
        else:
            print(f"Se encontraron {len(resultados)} vehículo(s):")
            for v in resultados:
                print(f"  {v}")