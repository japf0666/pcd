from functools import reduce
from typing import List

# Ejemplos de notas
notas = [90, 85, 92, 78, 88, 95, 84, 91, 79, 87, 57]
print(f"Notas originales: {notas}")

# Ej 1: Calcular las notas sobre 10 en vez de sobre 100 como están ahora.
    # Una primera función sin utilizar lambda y otra utilizando lambda
notas_10_scale = list(map(lambda x: x / 10, notas))
print(f"Notas sobre 10: {notas_10_scale}")

# Ej 2: Calcular la media de las notas
media_notas = reduce(lambda a, b: a + b, notas) / len(notas)
print(f"Media notas: {media_notas:.2f}")

# Ej 3: Convertir las notas a letras utilizando la siguiente tabla:
# A: 90-100
# B: 80-89
# C: 70-79
# D: 60-69
# F: 0-59
def convertir_a_letra(nota):
    if nota >= 90:
        return 'A'
    elif nota >= 80:
        return 'B'
    elif nota >= 70:
        return 'C'
    elif nota >= 60:
        return 'D'
    else:
        return 'F'

letter_notas = list(map(convertir_a_letra, notas))


# Ej 4: Filtrar las notas para quedarnos con las que son mayores o iguales a 60
passing_notas = list(filter(lambda x: x >= 60, notas))


# Muestra de resultados
print(f"Notas originales: {notas}")
print(f"Notas sobre 10: {notas_10_scale}")
print(f"Notas sobre 10 (lambda): {notas_10_scale}")
print(f"Media notas: {media_notas:.2f}")
print(f"Letra notas: {letter_notas}")
print(f"Notas aprobadas: {passing_notas}")


# Ej 5: Calcular la media de las notas con esta 
# estructura de diccionario.
personas = [
    {'Nombre': 'Alicia', 'Nota': 76},
    {'Nombre': 'Juan', 'Nota': 85},
    {'Nombre': 'Antonio', 'Nota': 89},
    {'Nombre': 'Carmen', 'Nota': 92}
]

media_notas_dict = reduce(lambda acc, persona: acc + persona['Nota'], personas, 0) / len(personas)
print(f"Media notas dict: {media_notas_dict:.2f}")
#