import random
from numeracion import Ubicacion

class Caza_Estelar:
    def __init__(self, dotacion: int, estado_ataque: bool):
        self.__dotacion = dotacion
        self.estado_ataque = estado_ataque
       # self.ubicacionAtaques 
      
    def mostrar_info(self):
        print(self)

    def isPossible_Star_Attack(self, ubicacionAtaque: Ubicacion) -> bool:
      if(self.__dotacion > 100 and ubicacionAtaque == Ubicacion.ENDOR):
        return True
      else:
        valor = random.choice([True, False])
        return valor
        
    def iniciar_ataque(self, ubicacionAtaque: Ubicacion) -> str:
       # self.ubicacionAtaques = ubicacionAtaque
        if(self.isPossible_Star_Attack(ubicacionAtaque)):
            self.estado_ataque = True
        else:
            self.estado_ataque = False
        if(self.estado_ataque): return( "El ataque fue exitoso")
        else: 
           return( "El ataque fallo o no fue posible")
      
    
    def __str__(self):
        return f" --> DOTACION: {self.__dotacion} | ESTADO DE ATAQUE actual: {self.estado_ataque} <--"

