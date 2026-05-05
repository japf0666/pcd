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
    destructor = NaveEstelar("Ejecutor", "ID-001", 123, 250000, 38000, EClaseNave.EJECUTOR)
    destructor2 = NaveEstelar("Ejecutor2", "ID-002", 1234, 250000, 38000, EClaseNave.EJECUTOR)

    sistema.registrar_almacenes(base_endor)
    sistema.registrar_naves(destructor)
    sistema.registrar_naves(destructor2)
    
    cmd_vader = Comandante("CMD-01", "Darth Vader", destructor)
    op_tk421 = Operario("OP-99", "Soldado TK-421", base_endor)
    admin = Admin("ADMIN", "ADMIN")
    cmd_sidious = Comandante("CMD-02", "Darth Sidious", destructor2)
    
    sistema.registrar_usuario(cmd_vader)
    sistema.registrar_usuario(op_tk421)
    sistema.registrar_usuario(admin)
    sistema.registrar_usuario(cmd_sidious)
    
    repuesto_inicial = Repuesto("Deflector", "Sienar", 10, 1500.0)
    base_endor.agregar_repuesto(repuesto_inicial)


def iniciar_consola(sistema):

    while True:
        print("===========================================")
        print("  sistema imperial")
        print("===========================================")

        usuario_actual = sistema.get_usuario_activo()

        # menu iniciar sesion 
        if usuario_actual is None:
            print("1. Iniciar Sesión")
            print("2. Salir")
            opcion = input("\n Elige una opción: ")

            if opcion == "1":
                id_ingresado = input("Introducir ID de usuario: ")
                limpiar_pantalla()
                mensaje = sistema.iniciar_sesion(id_ingresado)

                #este "if mensaje" funciona pq la funcion iniciar_sesion devuelve un str
                #si no existe no devuelve nada, por lo que es un 0 
                if mensaje:
                    print(f"\n{mensaje}")
                else:
                    print("\nID no encontrado.")

            elif opcion == "2":
                print("\nSaliendo del sistema.")
                break
            else:
                print("\nOpción inválida.")

        # menu con sesion iniciada
        else:
            print("----------------------------------------------------------------------")
            print(f" Usuario: {usuario_actual.nombre} | Rol: {type(usuario_actual).__name__}")
            print("----------------------------------------------------------------------")

            try:
                # menu de COMANDANTE
                if isinstance(usuario_actual, Comandante):
                    print("1. Encontrar repuesto")
                    print("2. Adquirir repuesto")
                    print("3. Consultar nave")
                    print("4. Mandar mensaje")
                    print("5. leer mensaje")
                    print("6. Cerrar sesión")
                    opcion = input("\nElige una opción: ")
                    
                    if opcion == "1":
                        pieza = input("Nombre de la pieza a buscar: ")
                        
                        resultados = sistema.encontrar_repuesto(pieza)
                        if isinstance(resultados, list):
                            for r in resultados:
                                print(f"  - {r}")
                        else:
                            print(f"  - {resultados}")
                            
                    elif opcion == "2":
                        pieza = input("Nombre de la pieza: ")
                        almacen = input("Nombre del almacén origen: ")
                        cant = int(input("Cantidad: "))

                        print(f"\n{sistema.adquirir_repuesto(pieza, almacen, cant)}")
                        
                    elif opcion == "3":
                        print(sistema.consultar_nave())
                    
                    elif opcion == "4":
                        print("\n--- ENVIAR TRANSMISIÓN ---")
                        try:
                            clave = int(input("Clave de transmisión destino: "))
                            mensaje = input("Mensaje a enviar: ")
                            
                            print(f"\n{sistema.enviar_mensaje(clave, mensaje)}")
                            
                        except ValueError:
                            print("\nError: La clave secreta debe ser un número entero.")
                            
                    elif opcion == "5":
                        mensajes = sistema.consultar_mensajes()
                        
                        if not mensajes:
                            print("\nBandeja de entrada vacía.")
                        else:
                            print(f"\n--- MENSAJES RECIBIDOS ---\n{mensajes}")
                                
                    elif opcion == "6":
                        sistema.cerrar_sesion()
                        limpiar_pantalla()

                # Menu de OPERARIO
                elif isinstance(usuario_actual, Operario):
                    print("1. Crear nuevo repuesto")
                    print("2. Actualizar stock")
                    print("3. Consultar almacen")
                    print("4. Cerrar sesion")
                    
                    opcion = input("\n Elige una opción: ")
                    
                    if opcion == "1":
                        nombre = input("Nombre del repuesto: ")
                        prov = input("Proveedor: ")
                        cant = int(input("Stock inicial: "))
                        coste = float(input("Coste unitario: "))
                        print(f"\n[+] {sistema.crear_repuesto(nombre, prov, cant, coste)}")
                        
                    elif opcion == "2":
                        nombre = input("Nombre del repuesto: ")
                        cant = int(input("Cantidad a sumar: "))
                        print(f"\n{sistema.actualizar_stock(nombre, cant)}")
                        
                    elif opcion == "3":
                        print(sistema.consultar_almacen())

                    elif opcion == "4":
                        sistema.cerrar_sesion()

                # menu de ADMIN
                elif isinstance(usuario_actual, Admin):
                    print("1. Crear comandante")
                    print("2. Crear operario")
                    print("3. Crear nave")
                    print("4. Crear almacen")
                    print("5. Lista Usuarios")
                    print("6. Lista naves")
                    print("7. Lista Almacenes")
                    print("8. Cerrar sesion")
                    
                    opcion = input("\nElige una opción: ")

                    if opcion == "1":
                        identificacion = input("Introduce su ID: ")
                        nombre = input("Introduce su nombre: ")
                        
                        naves = sistema.get_naves()
                        if not naves:
                            print("\nNo hay naves registradas. Crea una nave primero.")
                        else:
                            print("\nNaves disponibles:")
                            for nave in naves:
                                print(f"{nave.get_nombre()}")
                            
                            nombre_nave = input("\n Escribe el nombre de la nave: ")
                            nave_encontrada = None
                            
                            for n in naves:
                                if n.get_nombre() == nombre_nave:
                                    nave_encontrada = n
                                    break
                            
                            if nave_encontrada:
                                nuevo_cmd = Comandante(identificacion, nombre, nave_encontrada)
                                sistema.registrar_usuario(nuevo_cmd)
                                print(f"\nComandante '{nombre}' registrado a la nave '{nombre_nave}'.")
                            else:
                                print("\nNave no encontrada")

                    elif opcion == "2":
                        identificacion = input("Introduce su ID: ")
                        nombre = input("Introduce su nombre: ")
                        
                        almacenes = sistema.get_almacenes()
                        if not almacenes:
                            print("\nNo hay almacenes registrados. Crea uno primero.")
                        else:
                            print("\nAlmacenes disponibles:")
                            for almacen in almacenes:
                                print(f"  - {almacen.get_nombre()}")
                                
                            nombre_alm = input("\nEscribe el nombre del almacen")
                            alm_encontrado = None
                            
                            for almacen in almacenes:
                                if almacen.get_nombre() == nombre_alm:
                                    alm_encontrado = almacen
                                    break
                                    
                            if alm_encontrado:
                                nuevo_op = Operario(identificacion, nombre, alm_encontrado)
                                sistema.registrar_usuario(nuevo_op)
                                print(f"\nOperario '{nombre}' registrado al almacen '{nombre_alm}'.")
                            else:
                                print("\nAlmacén no encontrado")

                    elif opcion == "3":

                        #solo hago el metodo para crear un tipo de nave, por redundancia

                        nombre = input("Nombre de la nave: ")
                        identificador = input("Identificador: ")
                        clave = int(input("Clave: "))
                        tripulacion = int(input("Tripulacion: "))
                        pasaje = int(input("Pasaje: "))

                        nueva_nave = NaveEstelar(nombre, identificador, clave, tripulacion, pasaje, EClaseNave.EJECUTOR)
                        sistema.registrar_naves(nueva_nave)
                        print(f"\nNave '{nombre}' registrada")

                    elif opcion == "4":
                        nombre = input("Nombre del almacén: ")
                        localizacion = input("Localización: ")
                        
                        nuevo_almacen = Almacen(nombre, localizacion)
                        sistema.registrar_almacenes(nuevo_almacen)
                        print(f"\nAlmacén '{nombre}' registrado en {localizacion}.")

                    elif opcion == "5":
                        usuarios_registrados = sistema.get_usuarios()
                        
                        if not usuarios_registrados:
                            print("\nNo hay usuarios en el sistema.")
                        else:
                            print("----------------------")
                            print("\n   Lista de usuarios")
                            print("ID    |    NOMBRE    |    ROL   |")
                            for u in usuarios_registrados:
                                print(f"ID: {u.ID} | Nombre: {u.nombre} | Rol: {type(u).__name__}")

                    elif opcion == "6":
                        naves = sistema.get_naves()
                        if not naves:
                            print("No hay naves en el sistema.")
                        else:
                            print("----------------------")
                            print("\n   Lista de naves")
                            for n in naves:
                                print(f"Nombre: {n.get_nombre()} | Tipo: {type(n).__name__} | Clave: {n.get_clave()}")

                    elif opcion == "7":
                        almacenes = sistema.get_almacenes()
                        if not almacenes:
                            print("No hay almacenes en el sistema.")
                        else:
                            print("----------------------")
                            print("\n   Lista de almacenes")
                            for a in almacenes:
                                print(f"Nombre: {a.get_nombre()} | Localización: {a.get_localizacion()}")

                    elif opcion == "8":
                        sistema.cerrar_sesion()
                        limpiar_pantalla()
                        
                    else:
                        print("\nOpción no válida.")


            except (AccesoDenegadoError, StockInsuficienteError, ValueError) as e:
                print(f"\nERROR: {e}")
            except Exception as e:
                print(f"\nERROR DEL CODIGO: {e}")


if __name__ == "__main__":
    mi_sistema = Sistema()
    cargar_datos(mi_sistema)
    iniciar_consola(mi_sistema)



