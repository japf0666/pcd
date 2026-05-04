from almacen import Almacen
import almacen
from repuesto import Repuesto
from numeracion import Ubicacion, ClaseNave
from nave_estelar import Nave_Estelar
from estacion_espacial import Estacion_espacial
from caza_estelar import Caza_Estelar

def opciones_usuario(decision: str, almacen: Almacen, rol: str):

    if rol == "2":
        match decision:
            case "1":
                nombre_repuesto = input("Ingresa el nombre del repuesto: ")
                fabricante = input("Ingresa el fabricante del repuesto: ")
                cantidad = int(input("Ingresa la cantidad del repuesto: "))
                precio = float(input("Ingresa el precio del repuesto: "))
                nuevo_repuesto = Repuesto(nombre_repuesto, fabricante, cantidad, precio)
                try:
                    almacen.añadir_repuesto(nuevo_repuesto)
                    print("Repuesto añadido exitosamente.")
                except ValueError as e:
                    print(e)
            case "2":
                nombre_repuesto = input("Ingresa el nombre del repuesto a eliminar: ")
                try:
                    almacen.eliminar_repuesto(nombre_repuesto)
                    print("Repuesto eliminado exitosamente.")
                except ValueError as e:
                   print(e)
            case "3":
                nombre_repuesto = input("Ingresa el nombre del repuesto para actualizar stock: ")
                cantidad = int(input("Ingresa la cantidad a añadir (positivo) o retirar (negativo): "))
                try:
                    almacen.actualizar_stock(nombre_repuesto, cantidad)
                    print("Stock actualizado exitosamente.")
                except ValueError as e:
                    print(e)
            case "4":
                almacen.mostrar_catalogo()
            case _:
                print("Opción no válida. Por favor, ingresa un número del 1 al 4.") 
    
    elif rol == "1":
        match decision:
            case "1":
                almacen.mostrar_catalogo()
            case "2":
                nombre_repuesto = input("Ingresa el nombre del repuesto que deseas adquirir: ")
                try:
                    cantidad = int(input("Ingresa la cantidad que deseas adquirir: "))
                    almacen.actualizar_stock(nombre_repuesto, -cantidad)
                    print("Repuesto adquirido exitosamente.")
                except ValueError as e:
                    print(e)



def main():
    #poblar información de almacenes

    almacen1 = Almacen("Almacen Imperial ENDOR", Ubicacion.ENDOR )
    almacen2 = Almacen("Almacen SubCuartel ENDOR", Ubicacion.ENDOR )

    almacen3 = Almacen("Almacen Imperial NEBULOSA", Ubicacion.NEBULOSA_KALIIDA )
    almacen4 = Almacen("Almacen SubCuartel NEBULOSA", Ubicacion.NEBULOSA_KALIIDA )

    almacen5 = Almacen("Almacen Imperial CUMULO", Ubicacion.CUMULO_RAIMOS )
    almacen6 = Almacen("Almacen SubCuartel CUMULO", Ubicacion.CUMULO_RAIMOS )


    #poblar información de repuestos
    r1 = Repuesto("Motor Hiperespacial", "Kuat Drive Yards", 10, 50000)
    r2 = Repuesto("Escudo Deflector", "Corellia Corp", 5, 20000)
    r3 = Repuesto("Cañón Láser", "BlasTech Industries", 20, 15000)
    r4 = Repuesto("Generador de Energía", "Sienar Fleet Systems", 8, 30000)
    r5 = Repuesto("Sistema de Navegación", "Incom Corporation", 12, 18000)
    r6 = Repuesto("Blindaje Reforzado", "MandalMotors", 6, 40000)
    r7 = Repuesto("Propulsor Iónico", "Cygnus Spaceworks", 15, 22000)
    r8 = Repuesto("Computadora de Vuelo", "Holowan Labs", 10, 12000)
    r9 = Repuesto("Sensor de Largo Alcance", "Arakyd Industries", 7, 25000)
    r10 = Repuesto("Sistema de Comunicaciones", "Czerka Corporation", 9, 14000)
    
    #poblar información de repuestos en almacenes

    almacen1.añadir_repuesto(r1)
    almacen1.añadir_repuesto(r2)
    almacen1.añadir_repuesto(r3)

    almacen2.añadir_repuesto(r4)
    almacen2.añadir_repuesto(r5)
    almacen2.añadir_repuesto(r6)

    almacen3.añadir_repuesto(r2)
    almacen3.añadir_repuesto(r4)
    almacen3.añadir_repuesto(r6)

    almacen4.añadir_repuesto(r8)
    almacen4.añadir_repuesto(r10)
    almacen4.añadir_repuesto(r1)

    almacen5.añadir_repuesto(r3)
    almacen5.añadir_repuesto(r4)
    almacen5.añadir_repuesto(r7)

    almacen5.añadir_repuesto(r1)
    almacen5.añadir_repuesto(r5)
    almacen5.añadir_repuesto(r9)



    #almacen.mostrar_catalogo()

    nombre = input("Ingresa tu nombre: ")
    rol = input("\nIngresa tu rol:\n (1)comandante\n (2)operario:\n(3)salir\n")
    almacen = input("\nIngresa el almacen al que deseas acceder:\n (1) Almacen Imperial ENDOR\n (2) Almacen SubCuartel ENDOR\n (3) Almacen Imperial NEBULOSA\n (4) Almacen SubCuartel NEBULOSA\n (5) Almacen Imperial CUMULO\n (6) Almacen SubCuartel CUMULO: ")
    
    
    if almacen == "1":
        almacenA = almacen1
    elif almacen == "2":
        almacenA = almacen2
    elif almacen == "3":
        almacenA = almacen3
    elif almacen == "4":
        almacenA = almacen4
    elif almacen == "5":
        almacenA = almacen5
    elif almacen == "6":
        almacenA = almacen6
    else:
        print("Opción no válida. Por favor, ingresa un número del 1 al 6.")

    while(rol != "3"):
        if rol == "1":
            print(f"¡Bienvenido, Comandante {nombre}! Aquí están las opciones disponibles del sistema:")
            decision1 = input("deseas: \n(1) Consultar repuestos \n(2) Adquirir repuestos ")
            opciones_usuario(decision1, almacenA, rol)
        elif rol == "2":
            print(f"¡Bienvenido, operario, {nombre}! que requieres en esta ocacion -->\n")
            decision2 = input("deseas: \n(1) añadir repuesto \n(2) eliminar repuesto \n(3) actualizar stock \n(4) mostrar catálogo \n\nIngresa el número de la acción que deseas realizar: ")
            opciones_usuario(decision2, almacenA, rol)
        rol = input("\n\n\nIngresa tu rol:\n (1)comandante\n (2)operario:\n(3)salir\n")
   



    print("\nValor total inventario:", almacenA.calcular_valor_total_inventario())

    print("\n\n--------------------------------------------------------\nSe creo la nave:\n")
    #crear nave y mostrar información
    nave = Nave_Estelar(100, 300, ClaseNave.EJECUTOR)
    nave.mostrar_info()
    print("Capacidad total:", nave.capacidad_total())

    print("\n\n--------------------------------------------------------\nSe creo la estación espacial:\n")
    #crear nave y mostrar información
    print("\n tripulacion, pasaje, Ubicacion\n")
    estacion = Estacion_espacial(50, 200, Ubicacion.ENDOR)
    estacion.mostrar_info()
    #mover estación a otra ubicación
    print("\n\n--------------------------------------------------------\nSe movio la estacion----->\n")
    estacion.mostrar_info()
    #crear nave y mostrar información
    estacion.mover_estacion(Ubicacion.NEBULOSA_KALIIDA)
    print("Después de mover:")
    estacion.mostrar_info()
    #crear caza estelar y mostrar información
    print("\n\n--------------------------------------------------------\nSe creo el caza estelar:\n")
    caza = Caza_Estelar(20, False)
    caza.mostrar_info()
    #iniciar ataque y mostrar resultado
    print("\n\n--------------------------------------------------------\nSe inicio un ataque desde el caza estelar :\n")
    print("""\n
         .   . .
       .  :. ' :  .
       :. . :  . :
   . :  '.  . :  . :
  '  : :  '  : :  '
    '  .  .  .  '
        '  '
\n\n""")
    resultado = caza.iniciar_ataque(Ubicacion.CUMULO_RAIMOS)
    print("Resultado del ataque:", resultado)


if __name__ == "__main__":
    main()