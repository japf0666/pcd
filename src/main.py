#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de UIInterface con AgenciaAlquiler.
Ejecuta este archivo para iniciar el menú interactivo.
"""

from alquiler_vehiculos import (
    AgenciaAlquiler, Coche, Bicicleta, Cliente, UIInterface
)

def main():
    # Crear agencia
    agencia = AgenciaAlquiler()
    
    # Añadir algunos vehículos de demostración (opcional)
    agencia.agregar_vehiculo(Coche("C001", "Toyota Corolla", 2022, 50.0, 4))
    agencia.agregar_vehiculo(Coche("C002", "Honda Civic", 2021, 55.0, 2))
    agencia.agregar_vehiculo(Bicicleta("B001", "Trek X-Caliber", 2023, 15.0, 21))
    agencia.agregar_vehiculo(Bicicleta("B002", "Specialized Hardrock", 2022, 12.0, 18))
    
    # Añadir algunos clientes de demostración (opcional)
    agencia.agregar_cliente(Cliente("CLI001", "Juan Pérez", "juan@email.com"))
    agencia.agregar_cliente(Cliente("CLI002", "María García", "maria@email.com"))
    
    # Crear interfaz y ejecutar
    ui = UIInterface(agencia)
    ui.ejecutar()

if __name__ == "__main__":
    main()
