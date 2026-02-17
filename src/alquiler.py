class Vehiculo:
    def __init__(self, vehículo_id, modelo, año, tarifa_diaria):
        self.vehículo_id = vehículo_id
        self.modelo = modelo
        self.año = año
        self.tarifa_diaria = tarifa_diaria
        self.is_available = True

    def alquiler (self):
        # Implementar código para marcar el vehículo como alquilado.
        self.is_available = False

    def return_vehicle(self):
        # Implementar código para marcar el vehículo como disponible.
        self.is_available = True

    def calcular_costo_alquiler(self, días):
        # Implementar código para calcular el costo del alquiler según la cantidad de días.
        return días * self.tarifa_diaria
    
    def __str__(self): 
        return "Vehiculo: " + str(self.vehículo_id) + ", " +  self.modelo + ", " +  str(self.año) + ", " +  str(self.tarifa_diaria) + ", " +  str(self.is_available)
    

class Coche(Vehiculo):
    def __init__(self, id_vehículo, modelo, año, tarifa_diaria, num_puertas):
        super().__init__(id_vehículo, modelo, año, tarifa_diaria)
        self.num_puertas = num_puertas

    def __str__(self):
        return "Coche: " + str(self.num_puertas) + ", " + super().__str__()

class Bicicleta(Vehiculo):
    def __init__(self, id_vehículo, modelo, año, tarifa_diaria, num_gears):
        super().__init__(id_vehículo, modelo, año, tarifa_diaria)
        self.num_gears = num_gears

    def __str__(self):
        return "Bicicleta: " + str(self.num_gears) + ", " + super().__str__()

class Cliente:
    def __init__(self, cliente_id, nombre):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.vehiculos_alquilados = []

    def alquiler_vehiculo(self, vehículo, días):
        # Implementar código para que un cliente alquile un vehículo
        vehículo.alquiler()
        self.vehiculos_alquilados.append((vehículo, días))

    def return_vehicle(self, vehículo):
        # Implementar código para que un cliente devuelva un vehículo
        vehículo.return_vehicle()
        self.vehiculos_alquilados = [(v, d) for v, d in self.vehiculos_alquilados if v != vehículo]

    def __str__(self):

        txt = "Cliente: " + str(self.cliente_id) + ", " + self.nombre + "\n"

        txt += "** Vehiculos Alquilados**\n"
        for v, d in self.vehiculos_alquilados:
            txt += str(v) + " --> " + str(d) + " días\n"

        return txt

class AgenciaAlquiler:
    def __init__( self):
        self.vehiculos = []
        self.clientes = []

    def add_vehicle(self, vehículo):
        # Implementar código para agregar un vehículo a la agencia
        self.vehiculos.append(vehículo)

    def add_customer(self, cliente):
        # Implementar código para agregar un cliente a la agencia
        self.clientes.append(cliente)

    def __str__(self):
        return "AgenciaAlquiler: " + self.vehiculos + ", " + self.nombclientesre 

    def __str__(self):
        txt = "AgenciaAlquiler: \n"
        txt += "** Vehiculos **\n"
        for vehiculo in self.vehiculos:
            txt += str(vehiculo) + "\n"
            
        txt += "** Clientes **\n"
        for cliente in self.clientes:
            txt += str(cliente) + "\n"        
            
        return txt

# Ejemplo de uso:
agencia_alquiler = AgenciaAlquiler()

coche1 = Coche(1, "Toyota Camry", 2022, 30.0, 4)
coche2 = Coche(2, "Honda Accord", 2021, 35.0, 4)

bicicleta1 = Bicicleta(3, "Bicicleta de montaña", 2020, 15.0, 21)
bicicleta2 = Bicicleta(4, "Bicicleta de carretera", 2021, 20.0, 18)

agencia_alquiler.add_vehicle(coche1)
agencia_alquiler.add_vehicle(coche2)
agencia_alquiler.add_vehicle(bicicleta1)
agencia_alquiler.add_vehicle(bicicleta2)

cliente1 = Cliente(101, "Alicia")
cliente2 = Cliente(102, "Bob")

agencia_alquiler.add_customer(cliente1)
agencia_alquiler.add_customer(cliente2)

cliente1.alquiler_vehiculo(coche1, 3)
cliente2.alquiler_vehiculo(bicicleta1, 2)

cliente1.return_vehicle(coche1)


print(str(agencia_alquiler))