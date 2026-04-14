import itertools
import operator

#Ejemplo de generation y list comprenhension
lista = ["  palabra ", "palabra2 \n", "  palabra3   "]

lista_limpia = [p.strip() for p in lista]
print(lista_limpia)

#Paso 1: limpiar los datos
iter_limpia= (p.strip() for p in lista)
#Paso 2: convertir en mayúsculas
lista_limpia_mayus= [p.upper() for p in iter_limpia]
print(lista_limpia_mayus)

#Ejemplos de funciones itertools
print(itertools.count(10))

for i in itertools.count(10):
    print(i)
    if i > 15:
        break
    
#for i in itertools.cycle([1,2,3,4]):
#    print(i)

for i in itertools.repeat(3, 4):
    print(i)

print("*"* 10)    
l = [1,6,8,4,5]

for i in itertools.accumulate(l):
    print(i)

print("*"* 10)    
#for i in itertools.chain('ABCD', [1,2,3,4], itertools.accumulate(l)):
#    print(i)

print("*"* 10)    
lista_a_recorrer= ['ABCD', [1,2,3,4], itertools.accumulate(l),"abc"]
for i in itertools.chain.from_iterable(lista_a_recorrer):
    print(i)
    
print("*"* 10)    
lista_eq = "realmadrid barcelona atletico".split()
copas_europa= [15,5,0]
for equipo_ganador in itertools.compress(lista_eq, [x>5 for x in copas_europa]):
    print(equipo_ganador)
    
print("*"* 10)    
valores_sensor_lst = [3,2,1,4,3,5,5,5,66,44,23,5,14]
valores_sensor_limpio_lst = list(itertools.dropwhile(lambda x : x <=5, valores_sensor_lst))
print(valores_sensor_limpio_lst)

print("*"* 10)    
valores_sensor_lst = [3,2,1,4,3,5,5,5,66,44,23,5,14]
valores_sensor_limpio_lst = list(itertools.filterfalse(lambda x : x <=5, valores_sensor_lst))
print(valores_sensor_limpio_lst)

print("*"* 10)    
valores_sensor_lst = [3,2,1,4,3,5,5,5,66,44,23,5,14]
valores_sensor_limpio_lst = list(filter(lambda x : x <=5, valores_sensor_lst))
print(valores_sensor_limpio_lst)

print("*"* 10)    
datos = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("b", 5), ("c", 6)] 
# Agrupar por la primera letra de cada tupla 
grupos = itertools.groupby(datos, key=lambda x: x[0]) 
for clave, grupo in grupos: 
    grupo_lst = list(grupo)
    suma_total = 0 
    for e in grupo_lst:
        suma_total += e[1]
    print(clave, grupo_lst, suma_total)
    
print("*"* 10)  
print(list(itertools.islice(datos,1,8,2)))
    
print("*"* 10)  
print(list(itertools.pairwise([34,45,56,34,23,12,89])))
for t_acc in itertools.pairwise([34,45,56,34,23,12,89]):
    if t_acc[1]-t_acc[0] > 12:
        print("ojo que hay demasiada aceleracion", t_acc)

print("*"* 10)  

lista_valores= [(3,4), (5,6), (1,2)] 
for i in itertools.starmap(operator.add, lista_valores):
    print(i)
    
lista_valores2= [5,3,8,6,44,55,6]

#Coge los primeros elementos que sean menor que 10

nueva_= []
for i in lista_valores2:
    if i < 10:
        nueva_.append(i)
    else:
        break
print(nueva_)

nueva_ = list(itertools.takewhile(lambda x: x < 10, lista_valores2))
print(nueva_)


a = [1,2,3,4]
b= 'hola adios s'.split() #['hola','adios','s']

for s in zip(a,b):
    print(s)

for s in itertools.zip_longest(a,b):
    print(s)
    
def realiza_operacion(tipo_operacion, num1, num2):
    
    if tipo_operacion == '+':
        return num1+num2
    elif tipo_operacion == '-':
        return num1-num2


frase = "espero que aprobeis todos"
palabras_= frase.split()
palabras_len_dict= dict(map(lambda palabra: (palabra,len(palabra)), palabras_))
print(palabras_len_dict)

import math
v = (3,4)
print(math.sqrt(sum(map(lambda x: x**2, v))))

notas= [5,7,2,9,9,8,7]

def obtener_nota_cualitativa(nota:float):
    if nota >= 9:
        return "SOB"
    elif nota >= 7:
        return "NOT"
    elif nota >= 5:
        return "APR"
    return "SUS"
    
print(list(map(obtener_nota_cualitativa,notas)))

def calcular_precio(piso:dict):
    precio = (piso['metros']*1000) + (piso['habitaciones']*5000) + (int(piso['garaje'])*15000) 
    precio = precio * (1-(2025-piso['año'])/100)


    if piso['zona']== 'B':
        precio = precio * 1.5
    
    piso['precio']= precio 
    return piso
    
def buscar_piso(lista_pisos:list, presupuesto:float):
    pisos_encontrados = list(filter(lambda piso: piso['precio'] <= presupuesto, map(calcular_precio, lista_pisos)))
    return pisos_encontrados





