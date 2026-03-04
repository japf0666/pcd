#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de GUInterface - Interfaz Gráfica con tkinter para AgenciaAlquiler.
Ejecuta este archivo para abrir la ventana gráfica.

Requisito: tkinter debe estar disponible (incluido en Python por defecto)
"""

import tkinter as tk
from GUInterface import GUInterface
from alquiler_vehiculos import (
    AgenciaAlquiler, Coche, Bicicleta, Cliente
)


def main():
    # Crear ventana raíz
    root = tk.Tk()
    
    # Crear instancia de AgenciaAlquiler
    agencia = AgenciaAlquiler()
    
    # Agregar datos de prueba (opcional)
    agencia.agregar_vehiculo(Coche("C001", "Toyota Corolla", 2022, 50.0, 4))
    agencia.agregar_vehiculo(Coche("C002", "Honda Civic", 2021, 55.0, 2))
    agencia.agregar_vehiculo(Bicicleta("B001", "Trek X-Caliber", 2023, 15.0, 21))
    agencia.agregar_vehiculo(Bicicleta("B002", "Specialized Hardrock", 2022, 12.0, 18))
    
    agencia.agregar_cliente(Cliente("CLI001", "Juan Pérez", "juan@email.com"))
    agencia.agregar_cliente(Cliente("CLI002", "María García", "maria@example.com"))
    agencia.agregar_cliente(Cliente("CLI003", "Carlos López", "carlos@example.com"))
    
    # Crear interfaz gráfica
    gui = GUInterface(root, agencia)
    
    # Iniciar loop de eventos
    root.mainloop()


if __name__ == "__main__":
    main()
