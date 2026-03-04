#2. Implemente un sistema que permita instanciar diferentes tipos de vehículos (automóviles, motocicletas, autobuses, etc.) de diferentes marcas (Renault, Seat, BMW, etc.) 

#SOLUCIÓN: Requiere del patrón Factory Method.


from abc import ABC, abstractmethod

# Clase base que define la interfaz del producto
class Vehiculo(ABC):
    @abstractmethod
    def descripcion(self):
        pass

# Clase concreta que implementa la interfaz Vehiculo para Automóviles
class Automovil(Vehiculo):
    def descripcion(self):
        return "Soy un Automóvil"

# Clase concreta que implementa la interfaz Vehiculo para Motocicletas
class Motocicleta(Vehiculo):
    def descripcion(self):
        return "Soy una Motocicleta"

# Clase Factory (fábrica) que define el método para crear vehículos
class FabricaVehiculos(ABC):
    @abstractmethod
    def crear_vehiculo(self):
        pass

# Subclase de FabricaVehiculos que implementa la creación de Automóviles
class FabricaAutomoviles(FabricaVehiculos):
    def crear_vehiculo(self):
        return Automovil()

# Subclase de FabricaVehiculos que implementa la creación de Motocicletas
class FabricaMotocicletas(FabricaVehiculos):
    def crear_vehiculo(self):
        return Motocicleta()

# Función principal para probar el patrón Factory Method
def main():
    fabrica_automoviles = FabricaAutomoviles()
    automovil = fabrica_automoviles.crear_vehiculo()
    print(automovil.descripcion())

    fabrica_motocicletas = FabricaMotocicletas()
    motocicleta = fabrica_motocicletas.crear_vehiculo()
    print(motocicleta.descripcion())

if __name__ == "__main__":
    main()
