#  Implementa un programa de cálculo de impuestos donde diferentes estrategias
#  de cálculo de impuestos pueden ser intercambiadas fácilmente.

#SOLUCION: ES necesario hacer uso del patrón Strategy.

from enum import Enum


class TaxStrategy:
    def calculate_tax(self, income: int) -> int:
        pass

class TipoDeclaracion(Enum):
    AUTONOMO = 1
    EMPLEADO = 2
    EMPRESA = 3

class CalculadoraImpuestos:
    def __init__(self, tipoDeclaracion: TipoDeclaracion):
        self.strategy = self.get_strategy(tipoDeclaracion)

    def get_strategy(self, 
                     tipoDeclaracion: TipoDeclaracion) -> TaxStrategy:
        
        if tipoDeclaracion == TipoDeclaracion.AUTONOMO:
            return TasaAutonomo()
        elif tipoDeclaracion == TipoDeclaracion.EMPRESA:
            return TasaEmpresa()
        elif tipoDeclaracion == TipoDeclaracion.EMPLEADO:
            return TasaProgresiva()
        
        return None

    def calculate_tax(self, income: int) -> int:
        return self.strategy.calculate_tax(income)

class TasaEmpresa(TaxStrategy):
    def calculate_tax(self, income: int) -> int:
        return (int) (income * 0.15)

class TasaProgresiva(TaxStrategy):
    def __init__(self):
        self.tramos = [
            (10000, 0.1),
            (50000, 0.2),
            (float('inf'), 0.3)
        ]

    def calculate_tax(self, income: int) -> int:
        tax = 0
        budget = income
        for tramo, tasa in self.tramos:
            if budget > tramo:
                tax += tramo * tasa
                budget -= tramo
            else:                
                tax += budget * tasa
                break       
        return (int) (tax)
        
class TasaAutonomo(TaxStrategy):
    def calculate_tax(self, income: int) -> int:
        if income > 10000:
            return 1000 + (int) ((income - 10000) * 0.1)
        return 1000

if __name__ == "__main__":
    income = 60000
    calculadoraImpuestos = CalculadoraImpuestos(TipoDeclaracion.AUTONOMO)
    print("Impuesto calculado usando la estrategia TasaAutonomo:", 
          calculadoraImpuestos.calculate_tax(income))
    
    calculadoraImpuestos = CalculadoraImpuestos(TipoDeclaracion.EMPLEADO)
    print("Impuesto calculado usando la estrategia TasaProgresiva:", 
          calculadoraImpuestos.calculate_tax(income))
    
    calculadoraImpuestos = CalculadoraImpuestos(TipoDeclaracion.EMPRESA)
    print("Impuesto calculado usando la estrategia TasaEmpresa:", 
          calculadoraImpuestos.calculate_tax(income))
