# Cuatro en raya.
# El tablero es una matriz de 6 filas y 7 columnas.

# En cada turno el jugador elige una columna y la ficha
# se coloca en la posición más baja disponible de esa columna.

fichas= ['o','x']

# Vamos a modelar el tablero como una matriz de 6 x 7 caracteres
# donde cada casilla puede tener los valores:  
# '_' casilla vacía
# 'o' ficha del jugador 1
# 'x' ficha del jugador 2
import os
from typing import List

def init_tablero() -> List[List[str]]:
    """
    Docstring for init_tablero
   
    :return: Description
    :rtype: List[List[str]]
    """
    tablero= []
    for i in range(6):
        fila= ['_'] * 7
        tablero.append(fila)
    return tablero

def mostrar_tablero(tablero):
    """
    Método que muestra el estado actual del tablero
    Parámetros:
    * tablero: dict con el tablero a mostrar
    """
    for fila in tablero:
        for celda in fila:
            print(celda,end='')
        print('\n')

def columna_llena(tablero, columna) -> bool:
    """
    Método que comprueba si una columna está llena
    Parámetros:
    * columna: int con la columna a comprobar
    * tablero: List[List[str]] con el estado actual del tablero
    :return: bool indicando si la columna está llena
    """
    if columna < 0 or columna > 6:
        return True

    if tablero[0][columna] != '_':
        return True
    return False

def insertar_ficha(tablero, columna, ficha) -> List:
    """
    Método que inserta una ficha en la columna indicada
    Parámetros:
    * columna: int con la columna donde insertar la ficha
    * ficha: str con la ficha a insertar ('o' o 'x')
    * tablero: List[List[str]] con el estado actual del tablero
    :return: List indicando la posición donde se ha insertado la ficha o una lista vacía si no se ha podido insertar
    """
    if columna_llena(tablero, columna) or columna < 0 or columna > 6:
        return []
   
    for fila in range(5,-1,-1):
        if tablero[fila][columna] == '_':
            tablero[fila][columna] = ficha
            return [fila, columna]
    return []

def jugada_ganadora(tablero, ficha) -> bool:
    """
    Método que permite determinar si los movimientos de un jugador
    le permite ganar una partida.
    Comprobar si hay 3 fichas en una fila, columna o diagonal.
    """

    # comprobamos que hay cuatro columnas consecutivas en la misma fila
    # con el valor de la ficha del jugador
    for fila in range(6):
        for col in range(4):
            if (tablero[fila][col] == ficha and
                tablero[fila][col+1] == ficha and
                tablero[fila][col+2] == ficha and
                tablero[fila][col+3] == ficha):
                return True
           
    # Comprobamos que hay cuatro filas consecutivas en la misma columna
    # con el valor de la ficha del jugador
    for col in range(7):
        for fila in range(3):
            if (tablero[fila][col] == ficha and
                tablero[fila+1][col] == ficha and
                tablero[fila+2][col] == ficha and
                tablero[fila+3][col] == ficha):
                return True

    # Comprobamos diagonales (de izquierda a derecha)
    for fila in range(3):
        for col in range(4):
            if (tablero[fila][col] == ficha and
                tablero[fila+1][col+1] == ficha and
                tablero[fila+2][col+2] == ficha and
                tablero[fila+3][col+3] == ficha):
                return True
    # Comprobamos diagonales (de derecha a izquierda)
    for fila in range(3):
        for col in range(3,7):
            if (tablero[fila][col] == ficha and
                tablero[fila+1][col-1] == ficha and
                tablero[fila+2][col-2] == ficha and
                tablero[fila+3][col-3] == ficha):
                return True
    return False    

#############################################################
# Desarrollo del juego.

tablero= init_tablero()
end_game= False
casillas_libres= 6*7
jugador_activo= 0
jugador_no_activo = 1

while casillas_libres > 0 and not end_game:

    # solicitamos movimiento al jugador activo
    columna = input(f"JUGADOR {jugador_activo}: \
                            Introduce columna: ")
   
    # procesamos la entrada
    posicion = insertar_ficha(tablero, int(columna), 'o' if jugador_activo == 0 else 'x')

    if len(posicion) == 0:
        # Movimiento no válido.
        frequency = 2000 # Set Frequency To 2500 Hertz
        duration = 1000 # Set Duration To 1000 ms == 1 second
        print('\a')
        print("Columna llena o inválida. Turno para el siguiente jugador")
    else:
        # Comprobamos si el jugador activo ha ganado
        if jugada_ganadora(tablero, 'o' if jugador_activo == 0 else 'x'):
            print(F"ENHORABUENA EL JUGADOR {jugador_activo} HA GANADO")
            end_game= True

    # Mostramos el tablero actualizado
    mostrar_tablero(tablero)

    # Actualizamos las variables del juego
    if not end_game:
        casillas_libres= casillas_libres -1
        jugador_activo = (jugador_activo+1) % 2
