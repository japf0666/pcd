from clases import *
from enums import *
from sistema import Sistema
from excepciones import *
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_datos(sistema):
    
    """
    Esto es para cargar un minimo de cosas con las que poder trabjar y 
    probar cosas
    """

    base_endor = Almacen("Almacen Central", "Endor")
    destructor = NaveEstelar("Ejecutor", "ID-001", 12345, 250000, 38000, EClaseNave.EJECUTOR)
    
    sistema.registrar_almacenes(base_endor)
    sistema.registrar_naves(destructor)
    
    cmd_vader = Comandante("CMD-01", "Darth Vader", destructor)
    op_tk421 = Operario("OP-99", "Soldado TK-421", base_endor)
    admin_jefe = Admin("ADMIN", "Administrador")
    
    sistema.registrar_usuario(cmd_vader)
    sistema.registrar_usuario(op_tk421)
    sistema.registrar_usuario(admin_jefe)
    
    repuesto_inicial = Repuesto("Deflector", "Sienar", 10, 1500.0)
    base_endor.agregar_repuesto(repuesto_inicial)

def iniciar_consola(sistema):
    while True:
        print("\n===========================================")
        print("             SISTEMA IMPERIAL")
        print("===========================================")

        usuario_actual = sistema.get_usuario_activo()

        if usuario_actual is None:
            print("1. Iniciar sesión")
            print("2. Salir")
            opcion = input("\nElige una opción: ")

            if opcion == "1":
                id_ingresado = input("Introduce ID de usuario: ")
                limpiar_pantalla()
                mensaje = sistema.iniciar_sesion(id_ingresado)

                if mensaje:
                    print(f"\n{mensaje}")
                else:
                    print("\nError: ID no encontrado.")

            elif opcion == "2":
                print("\nSaliendo del sistema...")
                break
            else:
                print("\nOpción inválida.")

        else:
            print("-" * 60)
            print(f"Usuario: {usuario_actual.nombre} | Rol: {type(usuario_actual).__name__}")
            print("-" * 60)

            try:
                if isinstance(usuario_actual, Comandante):
                    print("1. Encontrar repuesto")
                    print("2. Adquirir repuesto")
                    print("3. Consultar nave")
                    print("4. Cerrar sesión")
                    
                    opcion = input("\nElige una opción: ")
                    
                    if opcion == "1":
                        pieza = input("Nombre de la pieza a buscar: ")
                        resultados = sistema.encontrar_repuesto(pieza)
                        if isinstance(resultados, list):
                            for r in resultados:
                                print(f" - {r}")
                        else:
                            print(f" - {resultados}")
                            
                    elif opcion == "2":
                        pieza = input("Nombre de la pieza: ")
                        almacen = input("Nombre del almacén origen: ")
                        cant = int(input("Cantidad: "))
                        print(f"\nÉxito: {sistema.adquirir_repuesto(pieza, almacen, cant)}")
                        
                    elif opcion == "3":
                        print(f"\n{sistema.consultar_nave()}")
                    
                    elif opcion == "4":
                        sistema.cerrar_sesion()
                        limpiar_pantalla()

                elif isinstance(usuario_actual, Operario):
                    print("1. Crear nuevo repuesto")
                    print("2. Actualizar stock")
                    print("3. Consultar almacen")
                    print("4. Cerrar sesion")
                    
                    opcion = input("\nElige una opción: ")
                    
                    if opcion == "1":
                        nombre = input("Nombre del repuesto: ")
                        prov = input("Proveedor: ")
                        cant = int(input("Stock inicial: "))
                        coste = float(input("Coste unitario: "))
                        print(f"\nÉxito: {sistema.crear_repuesto(nombre, prov, cant, coste)}")
                        
                    elif opcion == "2":
                        nombre = input("Nombre del repuesto: ")
                        cant = int(input("Cantidad a sumar: "))
                        print(f"\nÉxito: {sistema.actualizar_stock(nombre, cant)}")
                        
                    elif opcion == "3":
                        print(f"\n{sistema.consultar_almacen()}")

                    elif opcion == "4":
                        sistema.cerrar_sesion()
                        limpiar_pantalla()

                elif isinstance(usuario_actual, Admin):
                    print("1. Crear comandante")
                    print("2. Crear operario")
                    print("3. Crear nave")
                    print("4. Crear almacen")
                    print("5. Cerrar sesion")
                    
                    opcion = input("\nElige una opción: ")

                    if opcion == "1":
                        identificacion = input("Introduce ID: ")
                        nombre = input("Introduce nombre: ")
                        
                        naves = sistema.get_naves()
                        if not naves:
                            print("\nNo hay naves registradas. Crea una nave primero.")
                        else:
                            print("\nNaves disponibles:")
                            for nave in naves:
                                print(f"- {nave.get_nombre()}")
                            
                            nombre_nave = input("\nNombre de la nave a asignar: ")
                            nave_encontrada = None
                            
                            for n in naves:
                                if n.get_nombre() == nombre_nave:
                                    nave_encontrada = n
                                    break
                            
                            if nave_encontrada:
                                nuevo_cmd = Comandante(identificacion, nombre, nave_encontrada)
                                sistema.registrar_usuario(nuevo_cmd)
                                print(f"\nComandante '{nombre}' asignado a la nave '{nombre_nave}'.")
                            else:
                                print("\nError: Nave no encontrada.")

                    elif opcion == "2":
                        identificacion = input("Introduce ID: ")
                        nombre = input("Introduce nombre: ")
                        
                        almacenes = sistema.get_almacenes()
                        if not almacenes:
                            print("\nNo hay almacenes registrados. Crea uno primero.")
                        else:
                            print("\nAlmacenes disponibles:")
                            for almacen in almacenes:
                                print(f"- {almacen.get_nombre()}")
                                
                            nombre_alm = input("\nNombre del almacén a asignar: ")
                            alm_encontrado = None
                            
                            for almacen in almacenes:
                                if almacen.get_nombre() == nombre_alm:
                                    alm_encontrado = almacen
                                    break
                                    
                            if alm_encontrado:
                                nuevo_op = Operario(identificacion, nombre, alm_encontrado)
                                sistema.registrar_usuario(nuevo_op)
                                print(f"\nOperario '{nombre}' asignado al almacén '{nombre_alm}'.")
                            else:
                                print("\nError: Almacén no encontrado.")

                    elif opcion == "3":
                        nombre = input("Nombre de la nave: ")
                        identificador = input("Identificador: ")
                        clave = int(input("Clave de transmisión: "))
                        tripulacion = int(input("Tripulación: "))
                        pasaje = int(input("Pasaje: "))

                        nueva_nave = NaveEstelar(nombre, identificador, clave, tripulacion, pasaje, EClaseNave.EJECUTOR)
                        sistema.registrar_naves(nueva_nave)
                        print(f"\nNave '{nombre}' registrada.")

                    elif opcion == "4":
                        nombre = input("Nombre del almacén: ")
                        localizacion = input("Localización: ")
                        
                        nuevo_almacen = Almacen(nombre, localizacion)
                        sistema.registrar_almacenes(nuevo_almacen)
                        print(f"\nAlmacén '{nombre}' registrado en {localizacion}.")

                    elif opcion == "5":
                        sistema.cerrar_sesion()
                        limpiar_pantalla()
                        
                    else:
                        print("\nOpción no válida.")

            except (AccesoDenegadoError, StockInsuficienteError, ValueError) as e:
                print(f"\nError: {e}")
            except Exception as e:
                print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    mi_sistema = Sistema()
    cargar_datos(mi_sistema)
    iniciar_consola(mi_sistema)