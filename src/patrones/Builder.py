# Implementa un sistema que permita construir pizzas con ingredientes específicos y 
# diferentes tamaños (pequeña, mediana y familiar). 

# SOLUCIÓN: Requiere del patrón Builder.


# Clase que representa el producto final a construir
class Pizza:
    def __init__(self):
        self.tipo = None
        self.tamaño = None
        self.masa = None
        self.salsa = None
        self.ingredientes = []

    def __str__(self):
        return f"Pizza {self.tipo} - Tamaño: {self.tamaño}, Masa: {self.masa}, Salsa: {self.salsa}, Ingredientes: {', '.join(self.ingredientes)}"

# Clase raiz  Builder que define métodos para construir las partes de la Pizza
class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def build_tipo(self):
        pass

    def build_tamaño(self):
        pass

    def build_masa(self):
        pass

    def build_salsa(self):
        pass

    def build_ingredientes(self):
        pass

# Builder concreto que implementa los métodos para construir una Pizza específica
class PizzaHawaianaBuilder(PizzaBuilder):
    def build_tipo(self):
        self.pizza.tipo = "Hawaiana"

    def build_tamaño(self):
        self.pizza.tamaño = "Mediana"

    def build_masa(self):
        self.pizza.masa = "Delgada"

    def build_salsa(self):
        self.pizza.salsa = "Tomate"

    def build_ingredientes(self):
        self.pizza.ingredientes = ["Jamón", "Piña", "Queso"]

# Director que utiliza el Builder para construir el objeto complejo
class Pizzeria:
    def __init__(self, builder):
        self.builder = builder

    def construir_pizza(self):
        self.builder.build_tipo()
        self.builder.build_tamaño()
        self.builder.build_masa()
        self.builder.build_salsa()
        self.builder.build_ingredientes()
        return self.builder.pizza

# Función principal para probar el patrón Builder
if __name__ == "__main__":
    # Creamos un builder específico para una Pizza Hawaiana
    builder_hawaiana = PizzaHawaianaBuilder()

    # Creamos un director (Pizzería) que utiliza el builder específico
    pizzeria = Pizzeria(builder_hawaiana)

    # La pizzería construye la pizza
    pizza_hawaiana = pizzeria.construir_pizza()

    # Mostramos la pizza construida
    print(pizza_hawaiana)

