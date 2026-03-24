# Implementa un sistema de manejo de solicitudes de empleados en una empresa, 
# donde cada solicitud puede ser manejada por un supervisor, gerente o director, 
# según su nivel de autoridad.

# SOLUCIÓN: Aplicamos patrón Chain of Responsibility.

# El patrón Chain of Responsibility permite que una solicitud sea manejada 
# por una cadena de objetos, donde cada objeto tiene la oportunidad 
# de manejar la solicitud o pasarla al siguiente objeto en la cadena. 

from abc import ABC, abstractmethod

class Request:
    def __init__(self, level):
        self.level = level


class Handler(ABC):
    def __init__(self, successor=None):
        '''El constructor de la clase Handler recibe un objeto successor, 
        que representa el siguiente manejador en la cadena.'''
        self.successor = successor

    @abstractmethod
    def handle_request(self, request: Request):
        pass

class Supervisor(Handler):
    def handle_request(self, request):
        if request.level == "Supervisor":
            print("La solicitud será manejada por un Supervisor.")
        elif self.successor:
            self.successor.handle_request(request)

class Manager(Handler):
    def handle_request(self, request):
        if request.level == "Manager":
            print("La solicitud será manejada por un Gerente.")
        elif self.successor:
            self.successor.handle_request(request)

class Director(Handler):
    def handle_request(self, request):
        if request.level == "Director":
            print("La solicitud será manejada por un Director.")
        elif self.successor:
            self.successor.handle_request(request)



if __name__ == "__main__":

    supervisor = Supervisor()
    manager = Manager(supervisor)
    director = Director(manager)

    sup_request = Request("Supervisor")
    man_request = Request("Manager")
    dir_request = Request("Director")

    director.handle_request(sup_request)
    director.handle_request(man_request)
    director.handle_request(dir_request)