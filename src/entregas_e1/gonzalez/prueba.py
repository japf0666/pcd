from enumeraciones import ClaseNaveEstelar, UbicacionEstacion
from naves import CazaEstelar, EstacionEspacial, NaveEstelar
from almacen_piezas import Almacen, Repuesto, OperarioAlmacen, Comandante
from miImperio import MiImperio

def main():
    # Crear una instancia de MiImperio
    imperio = MiImperio()

    # Crear un almacén
    almacen1 = Almacen("Almacén 1", "Tatooine")
    imperio.añadir_almacen(almacen1)

    # Crear naves
    nave_estelar = NaveEstelar("Nave Estelar 1", ["Motor", "Ala"], 
                               30, 40, ClaseNaveEstelar.EJECUTOR)
    estacion_espacial = EstacionEspacial("Estación Espacial 1", ["Luces", 
                                        "Generador"], 100, 200, 
                                        UbicacionEstacion.NEBULOSA_KALIIDA)
    caza_estelar = CazaEstelar("Caza Estelar 1", ["Cañón", "Motor de Propulsión"], 
                               1)
    
    imperio.añadir_nave(nave_estelar)
    imperio.añadir_nave(estacion_espacial)
    imperio.añadir_nave(caza_estelar)

    print("Naves en el Imperio:")
    for nave in imperio.mostrar_naves():
        print(nave)
    
    comandante1 = Comandante("Comandante 1", nave_estelar)
    comandante2 = Comandante("Comandante 2", estacion_espacial)
    comandante3 = Comandante("Comandante 3", caza_estelar)

    operario1 = OperarioAlmacen("Operario 1")

    almacen1.añadir_operario(operario1)
    almacen1.añadir_comandante(comandante1)
    almacen1.añadir_comandante(comandante2)
    almacen1.añadir_comandante(comandante3)

    repuesto1 = Repuesto("Motor", "Proveedor A", 10, 5000.0)
    repuesto2 = Repuesto("Ala", "Proveedor B", 5, 3000.0)
    repuesto3 = Repuesto("Cañón", "Proveedor C", 20, 2000.0)
    

    operario1.añadir_repuesto(repuesto1, almacen1)
    operario1.añadir_repuesto(repuesto2, almacen1)
    operario1.añadir_repuesto(repuesto3, almacen1)

    almacen1.mostrar_repuestos()

    print("- " * 20)
    # Probamos los metodos de operadores y comandantes con manejo de excepciones
    try:
        comandante3.adquirir_repuesto("Motor", 2, almacen1)
    except Exception as e:
        print(f"Error: {e}")
    
    print("- " * 20)
    try: 
        comandante2.consultar_repuesto("Ala", almacen1)
    except Exception as e:
        print(f"Error: {e}")
    
    print("- " * 20)
    try:
        operario1.buscar_repuesto("Ala", almacen1)
    except Exception as e:
        print(f"Error: {e}")

    print("- " * 20)
    try:
        print("Precio del Cañón antes de cambiarlo:")
        operario1.buscar_repuesto("Cañón", almacen1)
        operario1.cambiar_precio_repuesto("Cañón", 2500.0, almacen1)
        print("Precio del Cañón después de cambiarlo:")
        operario1.buscar_repuesto("Cañón", almacen1)
    except Exception as e:
        print(f"Error: {e}")

    print("- " * 20)
    try:
        operario1.retirar_repuesto(repuesto2, almacen1)
    except Exception as e:
        print(f"Error: {e}")
    
    print("- " * 20)
    try:
        print("Repuestos antes de reponer:")
        operario1.buscar_repuesto("Motor", almacen1)
        print("Repuestos después de reponer:")
        operario1.reponer_repuesto("Motor", 12, almacen1)
        operario1.buscar_repuesto("Motor", almacen1)
    except Exception as e:
        print(f"Error: {e}")

        
if __name__ == "__main__":
    main()

