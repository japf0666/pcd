# Genericidad

def cuadrado(x):
    return x**2

def cubo(x):
    return x**3

def ejecutar(funcion, x):
    return funcion(x)

print("Ejemplo de funciones genéricas")
print(ejecutar(cuadrado, 3))
print(ejecutar(cubo, 3))

# Asignación de funciones a variables
f1 = cuadrado
f2 = cubo

print("Ejemplo de asignación de funciones a variables")
print(f1(3))
print(f2(3))

# Funciones que devuelven funciones
def crear_potencia(n):
    def potencia(x):
        return x**n
    return potencia

print("Ejemplo de funciones que devuelven funciones")
cuadrado = crear_potencia(2)
cubo = crear_potencia(3)
print(cuadrado(3))
print(cubo(3))

# List comprehensions y genrators con funciones
line_list = ['  Linea 1\n', 'Linea 2  \n', '  Linea 3   \n', '']
stripped_lines_1 = [line.strip() for line in line_list]
stripped_lines_2 = [line.strip() for line in stripped_lines_1 if line != '']
stripped_lines_3 = (line.strip() for line in line_list)

print(stripped_lines_1)
print(stripped_lines_2)
print(stripped_lines_3)

# Embebimmiento.
from operator import add, sub

funcs = {
    '+': add,
    '-': sub,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}

for f in funcs:
    print(f"{f} (3, 4): {funcs[f](3, 4)}")

# Uso inmediato de funciones anónimas.
print((lambda x: x**2)(3))

# Como argumentos de funciones de orden superior.
def aplicar_funcion(funcion, x):
    return funcion(x)
print(aplicar_funcion(lambda x: x**3, 3))

# ejemplos con itertools
import itertools

from itertools import islice

print(list(itertools.islice(range(10), 8)))
print(list(itertools.islice(range(10), 2, 8)))
print(list(itertools.islice(range(10), 2, 8, 2 )))


# Ejemplos con map.
print(list(map(lambda x: x.upper(), ['hola', 'mundo'])))
print([x.upper() for x in ['hola', 'mundo']])
tuplas = [(2, 2), (3, 3), (4, 4)]
print(list(map(lambda x: x[0] + x[1], tuplas)))

from itertools import starmap
print(list(starmap(pow, tuplas)))

# Ejemplos con filter.
seq = [0, 1, 2, 3, 5, 8, 13, 21]
print(list(filter(lambda x: x % 2 != 0, seq)))
print([x for x in seq if x % 2 != 0])
print(list(filter(lambda x: x % 2 == 0, seq)))
print([x for x in seq if (lambda n: n%2)(x) == 0])

# Ejemplos con reduce.
from functools import reduce
print(reduce(lambda x, y: x + y, [1, 2, 3, 4]))
print(reduce(lambda x, y: x + y, [1, 2, 3, 4], 11))

# Ejemplos con zip
a = [1, 2, 3]
b = ['a', 'b', 'c']
c = [True, False, True]
l1 = list(zip(a, b))
for item in l1:
    print(item)
l2 = list(zip(a, b, c))
for item in l2:
    print(item)

print(all([1,1,1 ]))
print(all([1,0,1 ]))
print(any([0,0,0 ]))
print(any([0,1,0 ]))

# ejemplos con map, reduce y zip.

# función que recibe una frase y devuelve un diccionario con la cantidad de veces 
# que aparece cada palabra.
def longitud_palabras(frase):
    palabras = frase.split()
    return dict(zip(palabras, map(len, palabras)))

print(longitud_palabras("hola mundo hola"))

# función que calcula el modulo de un vector
def modulo_vector(vector):
    return reduce(lambda x, y: x + y**2, vector, 0)**0.5

print(modulo_vector([3, 4]))
print(modulo_vector([3, 4, 5]))

# función que reciba una lista de notas y devuelva la lista de calificaciones 
# correspondientes a esas notas.
def calificaciones(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    else:
        return 'F'
    
def convertir_calificaciones(scores):
    return list(zip(scores, map(calificaciones, scores)))

print(convertir_calificaciones([95, 85, 75, 65]))

# Cálculo de precios de viviendas.

pisos = [
    {'annio': 2000, 'metros': 50, 'habitaciones': 2, 'garaje': True, 'zona': 'A'},
    {'annio': 2010, 'metros': 70, 'habitaciones': 3, 'garaje': False, 'zona': 'B'},
    {'annio': 1980, 'metros': 100, 'habitaciones': 4, 'garaje': True, 'zona': 'A'},
    {'annio': 2005, 'metros': 60, 'habitaciones': 2, 'garaje': False, 'zona': 'C'},
    {'annio': 2015, 'metros': 80, 'habitaciones': 3, 'garaje': True, 'zona': 'B'},
]

factores_zona = {'A': 1.5, 'B': 1.2, 'C': 1.0}

def calcular_precio(piso):
    precio_base = 1000
    precio = precio_base * piso['metros'] + \
             (piso['habitaciones'] * 5000) + \
             (15000 if piso['garaje'] else 0) 
    return precio * factores_zona[piso['zona']] * (1 - (2026 - piso['annio']) * 0.01)

# función que recibe una lista de pisos y un precio máximo y devuelve una lista de pisos que cumplen con ese precio.
def filtrar_pisos(pisos, precio_maximo):
    l = list(filter(lambda piso: calcular_precio(piso) <= precio_maximo, pisos))
    for piso in l:
        piso['precio'] = calcular_precio(piso)
    return l

# igual que la función anterior pero utilizando list comprehensions.
def filtrar_pisos_comprehension(pisos, precio_maximo):
    l = [piso for piso in pisos if calcular_precio(piso) <= precio_maximo]
    for piso in l:
        piso['precio'] = calcular_precio(piso)
    return l

# igual que la función anterior pero utilizando genrators.
def filtrar_pisos_generator(pisos, precio_maximo):
    l = (piso for piso in pisos if calcular_precio(piso) <= precio_maximo)
    for piso in l:
        piso['precio'] = calcular_precio(piso)
    return list(l)

# Misma funcionalidad pero implementada con un closure.
def aniadir_precio(piso):
    piso['precio'] = calcular_precio(piso)
    return piso

def filtrar_pisos_closure(pisos, precio_maximo):
    def filtro(piso):
        return piso['precio'] <= precio_maximo
    
    return list(filter(filtro, map(aniadir_precio, pisos)))


pisos_filtrados = filtrar_pisos(pisos, 100000)
for piso in pisos_filtrados:
    print(f"Piso filtrado: {piso}")
print("---------------"*10)

pisos_filtrados = filtrar_pisos_comprehension(pisos, 100000)
for piso in pisos_filtrados:
    print(f"Piso filtrado: {piso}")
print("---------------"*10)

pisos_filtrados = filtrar_pisos_generator(pisos, 100000)
for piso in pisos_filtrados:
    print(f"Piso filtrado: {piso}")
print("--------------"*10)

pisos_filtrados = filtrar_pisos_closure(pisos, 100000)
for piso in pisos_filtrados:
    print(f"Piso filtrado: {piso}")
print("--------------"*10)
print()
print()

# función que reciba una muestra de números y devuelva los valores atípicos 
# (valores cuya puntuación típica sea mayor que 3 o menor que -3).
# La puntuación típica de un valor se obtiene restando la media y dividiendo por 
# la desviación típica de la muestra.
# Usaremos un closure para calcular la media y la desviación típica de la muestra
# y luego filtrar los valores atípicos.

from statistics import mean, stdev

def atipico(muestra):
    media = mean(muestra)
    desviacion = stdev(muestra)
    
    def es_atipico(x):
        puntuacion_tipica = (x - media) / desviacion
        return puntuacion_tipica > 3 or puntuacion_tipica < -3
    
    return es_atipico

def valores_atipicos(muestra):
    return list(filter(atipico(muestra), muestra))

muestra = [10, 12, 12, 13, 12, 11, 14, 13, 100, 500, 10000]
print(valores_atipicos(muestra))
print("--------------"*10)
print()

# Escriba una función que elimine todos los números de una lista menores 
# o iguales que el argumento indicado
def eliminar_menores(lista, umbral):
    return [x for x in lista if x > umbral]

muestra = [10, 12, 12, 13, 12, 11, 14, 13, 100, 500, 10000]
print(eliminar_menores(muestra, 50))
print("--------------"*10)

# Función que devuelva una lista con todos los números de la lista 
# de entrada que estén en el rango indicado por los dos primeros argumentos
def filtrar_por_rango(lista, minimo, maximo):
    return [x for x in lista if minimo <= x <= maximo]

muestra = [10, 12, 12, 13, 12, 11, 14, 13, 100, 500, 10000]
print(filtrar_por_rango(muestra, 20, 500))
print("--------------"*10)

# Función que reciba como argumento una lista y devuelva la lista que resulta 
# de filtrar los números pares de la lista y dividirlos entre 2, excluyendo a los impares.
def filtrar_pares_dividir(lista):
    return [x / 2 for x in lista if x % 2 == 0]

def filtrar_pares_dividir_map(lista):
    return list(map(lambda x: x / 2, filter(lambda x: x % 2 == 0, lista)))

muestra = [10, 12, 12, 13, 12, 11, 14, 13, 100, 500, 10000] 
print(filtrar_pares_dividir(muestra))
print("--------------"*10)
print(filtrar_pares_dividir_map(muestra))
print("--------------"*10)

# función que tome una lista de palabras como entrada y 
# devuelva la lista resultante después de filtrar las palabras que contienen más de cinco letras, 
# las convierta a mayúsculas y las ordene en orden alfabético inverso. 
def filtrar_palabras(palabras):
    return sorted([palabra.upper() for palabra in palabras if len(palabra) > 5], reverse=True)

palabras = ['hola', 'mundo', 'python', 'programacion', 'ejemplo', 'lambda']
print(filtrar_palabras(palabras))

# usando map, filter y sorted
def filtrar_palabras_map(palabras):
    return sorted(map(lambda x: x.upper(), filter(lambda x: len(x) > 5, palabras)), reverse=True)
print(filtrar_palabras_map(palabras))

# versión más expandida.

def filtrar_palabras_expanded(palabras):
    palabras_filtradas = filter(lambda x: len(x) > 5, palabras)
    palabras_mayusculas = map(lambda x: x.upper(), palabras_filtradas)
    return sorted(palabras_mayusculas, reverse=True)
print(filtrar_palabras_expanded(palabras))

# Implemente una función que tome como argumento un número entero, n, y 
# devuelva la lista de números primos menos que n y su suma. 
def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def primos_menores_que(n):
    primos = [x for x in range(2, n) if es_primo(x)]
    return primos, sum(primos)

print(primos_menores_que(20))

# Implemente una función que tome una lista de palabras como entrada y 
# devuelva la lista resultante después de filtrar palabras que contienen 
# más de cinco letras, y luego las convierta a mayúsculas
def filtrar_palabras_mayusculas(palabras):
    return [palabra.upper() for palabra in palabras if len(palabra) > 5]

palabras = ['hola', 'mundo', 'python', 'programacion', 'ejemplo', 'lambda']
print(filtrar_palabras_mayusculas(palabras))

# Versión con map y filter
def filtrar_palabras_mayusculas_map(palabras):
    return list(map(lambda x: x.upper(), filter(lambda x: len(x) > 5, palabras)))
print(filtrar_palabras_mayusculas_map(palabras))

# Implemente una función que tome una lista de palabras como entrada y devuelva 
# la lista resultante después de filtrarlas palabras que contienen alguna mayúscula 
# (puede usar any)
def filtrar_palabras_mayusculas_any(palabras):
    return [palabra for palabra in palabras \
            if any(c.isupper() for c in palabra)]

palabras = ['hola', 'mundo', 'Python', 'programacion', 'Ejemplo', 'lambda']
print(filtrar_palabras_mayusculas_any(palabras))

#version con filter y any
def filtrar_palabras_mayusculas_any_filter(palabras):
    return list(filter(lambda palabra: any(c.isupper() for c in palabra), palabras))

palabras = ['hola', 'mundo', 'Python', 'programacion', 'Ejemplo', 'lambda']
print(filtrar_palabras_mayusculas_any_filter(palabras))