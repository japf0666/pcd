# Crea un sistema donde varios usuarios puedan suscribirse a un servicio de 
# notificaciones y recibir actualizaciones cuando se publiquen nuevas noticias.


class Noticia:
    def __init__(self, titulo, categoria, prioridad):
        self.titulo = titulo
        self.categoria = categoria
        self.prioridad = prioridad


class Publicador:
    def __init__(self):
        self.suscriptores= []

    def alta(self, observer):
        self.suscriptores.append(observer)

    def baja(self, observer):
        self.suscriptores.remove(observer)

    def notificarSuscriptores(self, noticia):
        for suscriptor in self.suscriptores:
            suscriptor.actualizar(noticia)

#El observador
class Suscriptor:
    def actualizar(self, noticia):
        pass

class SuscriptorGeneral(Suscriptor):
    def __init__(self, nombre):
        self.nombre = nombre

    def actualizar(self, noticia):
        print(f"{self.nombre} recibió la notificación: {noticia.titulo}")


class SuscriptorDeportes(Suscriptor):
    def __init__(self, nombre):
        self.nombre = nombre

    def actualizar(self, noticia):
        if noticia.categoria == "Deportes":
            print(f"{self.nombre} está leyendo una noticia deportiva: {noticia.titulo}")

class SuscriptorImportante(Suscriptor):
    def __init__(self, nombre):
        self.nombre = nombre

    def actualizar(self, noticia):
        if noticia.prioridad >= 8:
            print(f"{self.nombre} recibió una noticia urgente: {noticia.titulo} (prioridad {noticia.prioridad})")


if __name__ == "__main__":
    publicador = Publicador()

    sub1 = SuscriptorGeneral("Usuario1")
    sub2 = SuscriptorDeportes("Carlos")
    sub3 = SuscriptorImportante("Ana")

    publicador.alta(sub1)
    publicador.alta(sub2)
    publicador.alta(sub3)

    noticia1 = Noticia("Partido final de la Champions", "Deportes", 7)
    noticia2 = Noticia("Terremoto en Chile", "Actualidad", 9)
    noticia3 = Noticia("Nueva actualización del sistema", "Tecnología", 5)

    publicador.notificarSuscriptores(noticia1)
    publicador.notificarSuscriptores(noticia2)
    publicador.notificarSuscriptores(noticia3)


