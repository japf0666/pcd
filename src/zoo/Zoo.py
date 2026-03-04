from enum import Enum

class EDieta(Enum):
        HERBIVORO = 1
        CARNIVORO = 2
        INSECTIVORO = 3
        OMNIVORO = 4
            
class Comida:
        
    def __init__ (self,nombre, dieta):
        self.nombre = nombre
        self.dieta = dieta
            
    def __str__(self):
        return "Comida: " + self.nombre + ", " + str(self.dieta)

class Stock:
        
    def __init__ (self):
        self.stock = dict() # La cantidad de cada comida
        self.dietas = dict() # las comidas de cada dieta
        
    def compra(self, comida, cantidad):
        if comida.nombre in self.stock:
           self.stock[comida.nombre] += cantidad
        else:
           self.stock[comida.nombre] = cantidad
           if comida.dieta in self.dietas:
               self.dietas[comida.dieta].append(comida)
           else:
               self.dietas[comida.dieta] = list([comida])

    def sacar(self, comida, cantidad):
        # Devuelve cuanta cantidad ha sido posible sacar del stock
        if comida in self.stock:
           if cantidad < self.stock[comida]:
               self.stock[comida] -= cantidad
               return cantidad
           else:
               # Se saca todo lo que queda
               c = self.stock[comida]
               self.stock[comida] = 0 # ahora no queda nada
               return c
        else:
            return 0

    def comidas(self, dieta):
        return self.comidas[dieta]

    def comidasPara(self, animal):
        return self.comidas(animal.dieta)

    def cantidad(self, comida):
        if comida in self.stock:
            return self.stock[comida]
        else:
            return 0

    def __str__(self):
        return "Stock: " + str(self.stock) + "\n" + str(self.comidas)

class Animal:

    def __init__ (self, id, especie, dieta):
        self.id = id        
        self.especie=especie
        self.dieta = dieta
        self.cuidador = None         
            
    def __str__(self):
        return "Animal: " + str(self.id) + ", " + self.especie + ", " + str(self.dieta)

    def tieneCuidador(self):
        return self.cuidador != None

    def asignarCuidador(self, cuidador):
        # Si es el mismo cuidador -> no hay que cambiar nada
        if self.cuidador == cuidador:
            return

        # Tiene asignado otro o ninguno
        if self.tieneCuidador():
            self.cuidador.quitarAnimal(self)

        self.cuidador = cuidador
        self.cuidador.asignarAnimal(self)

    def quitarCuidador(self):
        if self.tieneCuidador():
           cuidador = self.cuidador
           self.cuidador = None
           cuidador.quitarAnimal(self)

class Vacaciones:
       
    def __init__(self, inicio, duracion): 
        self.inicio=inicio
        self.duracion=duracion

class Cuidador:
        
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.animales = list()
        self.vacaciones = list()

    def cogeVacaciones(self, inicio, duracion):
        self.vacaciones.append(Vacaciones(inicio, duracion))

    def vacaciones(self):
        return self.vacaciones

    def asignarAnimal(self, animal):
        if animal in self.animales: # Ya lo tiene asignado
            return
        self.animales.append(animal)
        animal.asignarCuidador(self)

    def quitarAnimal(self, animal):
        if animal in self.animales:
            self.animales.remove(animal)
            animal.quitarCuidador()
    
    def __str__(self):
        txt = "Cuidador:" + self.nombre + " " + self.apellidos + "\n"
        for animal in self.animales:
            txt += str(animal) + "\n"

        for vaca in self.vacaciones:
            txt += str(vaca) + "\n"

        return txt

class Zoo:
        
    def __init__(self):
        self.cuidadores = list()
        self.animales = list()
        self.stock = Stock()
        self.idCont = 0

    def contratarCuidador(self, cuidador):
        self.cuidadores.append(cuidador)
            
    def contratar(self, nombre, apellidos):
        cuidador = Cuidador(nombre, apellidos)
        self.contratarCuidador(cuidador)
        return cuidador

    def adquirirAnimal(self, animal):
        self.animales.append(animal)

    def adquirir(self, especie, dieta):
        self.idCont += 1
        animal = Animal(self.idCont, especie, dieta)
        self.adquirirAnimal(animal)
        return animal

    def stock(self):
        return self.stock

    def __str__(self):
        txt = "Zoo: \n"
        txt += "** Cuidadores **\n"
        for cuidador in self.cuidadores:
            txt += str(cuidador) + "\n"
            
        txt += "** Animales **\n"
        for animal in self.animales:
            txt += str(animal) + "\n"

        txt += "** Stock **\n"
        for comida in self.stock.stock:
            txt += str(comida) + ": " + str(self.stock.cantidad(comida)) + " Kg\n"
            
        return txt

# Veamos ahora unos ejemplos de uso de estas clases
if __name__ == "__main__":

    # Creamos el objeto Zoo
    zoo = Zoo()

    # Creamos algunos alimentos
    carneVacuno = Comida("Vacuno", EDieta.CARNIVORO)
    carneCaza   = Comida("Caza",  EDieta.CARNIVORO)
    manzanas    = Comida("Manzanas", EDieta.HERBIVORO)
    platanos    = Comida("Platanos", EDieta.HERBIVORO)
    larvas      = Comida("Larvas", EDieta.INSECTIVORO)

    # El zoo compra cantidades de estos alimentos
    zoo.stock.compra(carneVacuno, 50)
    zoo.stock.compra(manzanas, 10)
    zoo.stock.compra(platanos, 10)
    zoo.stock.compra(larvas, 5)

    # El zoo adquiere algunos animales
    tigre = zoo.adquirir("Tigre", EDieta.CARNIVORO)
    leon = zoo.adquirir("Leon", EDieta.CARNIVORO)
    elefante = zoo.adquirir("Elefante", EDieta.HERBIVORO)
    hipopotamo = zoo.adquirir("Hipopotamo", EDieta.HERBIVORO)
    cebra = zoo.adquirir("Cebra", EDieta.HERBIVORO)
    cocodrilo = zoo.adquirir("Cocodrilo", EDieta.CARNIVORO)

    # El zoo contrata a algunos cuidadores
    juan = zoo.contratar("Juan", "Abellan Lopez")
    pepe = zoo.contratar("Pepe", "Garcia Sanchez")
    laura = zoo.contratar("Laura", "Perez Ramirez")

    # Asignar animales a cuidadores
    juan.asignarAnimal(tigre)
    juan.asignarAnimal(leon)
    pepe.asignarAnimal(elefante)
    pepe.asignarAnimal(cebra)
    laura.asignarAnimal(hipopotamo)
    laura.asignarAnimal(cocodrilo)

    # mostrar el estado actual del zoo
    
    print(str(zoo))

    
