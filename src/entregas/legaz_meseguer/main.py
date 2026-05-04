"""
SISTEMA CONTROL DE FLUJO DE USUARIOS, UNIDADES Y ALMACENES
"""

from src.usuarios.usuario import Comandante, Opeario
from src.logistica.almacen import Almacen

from src.logistica.repuesto import Repuesto
from src.utils.enumeraciones import Ubicacion, ClaseNaveEstelar


# ============================================================================
# INICIALIZACIÓN DEL SISTEMA
# ============================================================================

# Diccionario de usuarios registrados
usuarios = {}

# Crear almacenes de demostración
almacen_principal = Almacen("Almacén Principal", "Estación Espacial Central")
almacen_secundario = Almacen("Almacén Secundario", "Base Lunar")

#Creando ususario para demostracion:
usuario_1 = Comandante('Jesus Benitez','jesus_Benitez')
usuario_2 = Opeario('Julia Garcia', 'julita_gar')

# Crear repuestos de demostración
repuesto1 = Repuesto("Alas Propulsoras", "Techno Industrial", 15, 1500.0)

repuesto2 = Repuesto("Misiles Atómicos", "Corporación Estelar", 8, 3000.0)

repuesto3 = Repuesto("Placas Solares", "SolidState Systems", 25, 800.0)

# Agregar repuestos a almacenes
almacen_principal.inventario.append(repuesto1)
almacen_principal.inventario.append(repuesto2)
almacen_principal.inventario.append(repuesto3)

almacen_secundario.inventario.append(repuesto1)
almacen_secundario.inventario.append(repuesto3)

usuarios['jesus_Benitez'] = usuario_1
usuarios['julita_gar'] = usuario_2

almacenes = [almacen_principal, almacen_secundario]


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    import os

    os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("    SISTEMA DE CONTROL DE FLUJO - IMPERIO GALÁCTICO")
    print("=" * 60)
    print("(1) Iniciar Sesión")
    print("(2) Registrarse")
    print("(9) Salir")
    print("=" * 60)


def registrar_usuario():
    """Registra un nuevo usuario en el sistema"""
    limpiar_pantalla()
    print("\n--- REGISTRO DE USUARIO ---")

    usuario_id = input("Ingrese su ID de usuario (único): ").strip()

    # Validar que el usuario no exista
    if usuario_id in usuarios:
        print(f"Error: El usuario '{usuario_id}' ya está registrado.")
        input("Presione Enter para continuar...")
        return

    # Solicitar tipo de usuario
    print("\n(1) Comandante - Acceso a consulta y compra de repuestos")
    print("(2) Operario - Acceso a gestión de inventario")

    tipo = input("Seleccione su tipo de usuario (1 o 2): ").strip()

    if tipo == "1":
        usuario = Comandante(f"Comandante {usuario_id}", usuario_id)
        usuarios[usuario_id] = usuario
        print(f"¡Comandante '{usuario_id}' registrado exitosamente!")
        input("Presione Enter para continuar...")
    elif tipo == "2":
        usuario = Opeario(f"Operario {usuario_id}", usuario_id)
        usuarios[usuario_id] = usuario
        print(f"¡Operario '{usuario_id}' registrado exitosamente!")
        input("Presione Enter para continuar...")
    else:
        print("Opción inválida. Intente de nuevo.")
        input("Presione Enter para continuar...")


def iniciar_sesion():
    """Inicia sesión de un usuario existente"""
    limpiar_pantalla()
    print("\n--- INICIO DE SESIÓN ---")

    usuario_id = input("Ingrese su ID de usuario: ").strip()

    if usuario_id not in usuarios:
        print(f"Error: Usuario '{usuario_id}' no encontrado.")
        import time

        time.sleep(2)
        limpiar_pantalla()
        return None

    usuario = usuarios[usuario_id]
    print(f"¡Bienvenido {usuario.nombre}!")
    import time

    time.sleep(1)
    limpiar_pantalla()
    return usuario


def menu_comandante(comandante):
    """Menú específico para Comandantes"""
    while True:
        limpiar_pantalla()
        print("\n" + "=" * 60)
        print(f"    MENÚ COMANDANTE - {comandante.id_usuario}")
        print("=" * 60)
        print("(1) Consultar repuesto en almacén")
        print("(2) Adquirir repuesto")
        print("(3) Listar almacenes disponibles")
        print("(4) Cerrar sesión")
        print("=" * 60)

        opcion = input("Elige tu opción: ").strip()

        if opcion == "1":
            menu_consultar_repuesto(comandante)
        elif opcion == "2":
            menu_adquirir_repuesto(comandante)
        elif opcion == "3":
            limpiar_pantalla()
            listar_almacenes()
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            print(f"\nHasta luego {comandante.nombre}!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            input("Presione Enter para continuar...")


def menu_operario(operario):
    """Menú específico para Operarios"""
    while True:
        limpiar_pantalla()
        print("\n" + "=" * 60)
        print(f"    MENÚ OPERARIO - {operario.id_usuario}")
        print("=" * 60)
        print("(1) Registrar repuesto en almacén")
        print("(2) Actualizar stock de repuesto")
        print("(3) Listar almacenes disponibles")
        print("(4) Cerrar sesión")
        print("=" * 60)

        opcion = input("Elige tu opción: ").strip()

        if opcion == "1":
            menu_registrar_repuesto(operario)
        elif opcion == "2":
            menu_actualizar_stock(operario)
        elif opcion == "3":
            limpiar_pantalla()
            listar_almacenes()
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            print(f"\nHasta luego {operario.nombre}!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            input("Presione Enter para continuar...")


def listar_almacenes():
    """Lista todos los almacenes disponibles"""
    print("\n--- ALMACENES DISPONIBLES ---")
    for idx, almacen in enumerate(almacenes, 1):
        print(f"\n({idx}) {almacen.nombre}")
        print(f"    Ubicación: {almacen.localizacion}")
        print(f"    Repuestos en stock: {len(almacen.inventario)}")
        for rep in almacen.inventario:
            print(f"       • {rep.nombre} ({rep.get_cantidad()} unidades)")


def menu_consultar_repuesto(comandante):
    """Menú para que el Comandante consulte repuestos"""
    limpiar_pantalla()
    print("\n--- CONSULTAR REPUESTO ---")

    listar_almacenes()

    try:
        almacen_idx = int(input("\nSeleccione número de almacén: ")) - 1
        if 0 <= almacen_idx < len(almacenes):
            almacen = almacenes[almacen_idx]
            nombre_pieza = input("Nombre de la pieza a consultar: ").strip()
            comandante.consultar_repuesto(nombre_pieza, almacen)
            input("\nPresione Enter para continuar...")
        else:
            print("Almacén inválido.")
            input("Presione Enter para continuar...")
    except ValueError:
        print("Error: Ingrese un número válido.")
        input("Presione Enter para continuar...")


def menu_adquirir_repuesto(comandante):
    """Menú para que el Comandante adquiera repuestos"""
    limpiar_pantalla()
    print("\n--- ADQUIRIR REPUESTO ---")

    listar_almacenes()

    try:
        almacen_idx = int(input("\nSeleccione número de almacén: ")) - 1
        if 0 <= almacen_idx < len(almacenes):
            almacen = almacenes[almacen_idx]
            nombre_pieza = input("Nombre de la pieza a adquirir: ").strip()
            comandante.adquirir_repuesto(nombre_pieza, almacen)
            input("\nPresione Enter para continuar...")
        else:
            print("Almacén inválido.")
            input("Presione Enter para continuar...")
    except ValueError:
        print("Error: Ingrese un número válido.")
        input("Presione Enter para continuar...")


def menu_registrar_repuesto(operario):
    """Menú para que el Operario registre nuevos repuestos"""
    limpiar_pantalla()
    print("\n--- REGISTRAR NUEVO REPUESTO ---")

    try:
        nombre = input("Nombre del repuesto: ").strip()
        proveedor = input("Proveedor: ").strip()
        cantidad = int(input("Cantidad inicial: "))
        precio = float(input("Precio: "))

        nuevo_repuesto = Repuesto(nombre, proveedor, cantidad, precio)

        listar_almacenes()
        almacen_idx = int(input("\nSeleccione número de almacén: ")) - 1

        if 0 <= almacen_idx < len(almacenes):
            almacen = almacenes[almacen_idx]
            operario.registrar_repuesto(nuevo_repuesto, almacen)
            print(f"Repuesto '{nombre}' registrado exitosamente.")
            input("Presione Enter para continuar...")
        else:
            print("Almacén inválido.")
            input("Presione Enter para continuar...")
    except ValueError:
        print("Error: Ingrese valores válidos.")
        input("Presione Enter para continuar...")


def menu_actualizar_stock(operario):
    """Menú para que el Operario actualice stock de repuestos"""
    limpiar_pantalla()
    print("\n--- ACTUALIZAR STOCK ---")

    listar_almacenes()

    try:
        almacen_idx = int(input("\nSeleccione número de almacén: ")) - 1
        if 0 <= almacen_idx < len(almacenes):
            almacen = almacenes[almacen_idx]
            nombre_pieza = input("Nombre del repuesto: ").strip()

            # Buscar el repuesto
            repuesto_encontrado = None
            for rep in almacen.inventario:
                if rep.nombre.lower() == nombre_pieza.lower():
                    repuesto_encontrado = rep
                    break

            if repuesto_encontrado:
                nueva_cantidad = int(input("Nueva cantidad: "))
                operario.actualizar_stock(repuesto_encontrado, nueva_cantidad)
                print(f"Stock de '{nombre_pieza}' actualizado a {nueva_cantidad}.")
                input("Presione Enter para continuar...")
            else:
                print(f"Repuesto '{nombre_pieza}' no encontrado en este almacén.")
                input("Presione Enter para continuar...")
        else:
            print("Almacén inválido.")
            input("Presione Enter para continuar...")
    except ValueError:
        print("Error: Ingrese valores válidos.")
        input("Presione Enter para continuar...")


# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    limpiar_pantalla()
    while True:
        mostrar_menu_principal()
        opcion = input("Elige tu opción: ").strip()

        if opcion == "1":
            usuario = iniciar_sesion()
            if usuario is not None:
                if isinstance(usuario, Comandante):
                    menu_comandante(usuario)
                else:
                    menu_operario(usuario)
                limpiar_pantalla()
        elif opcion == "2":
            registrar_usuario()
            limpiar_pantalla()
        elif opcion == "9":
            limpiar_pantalla()
            print("\n¡That's all folks! Abandonando el sistema...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            import time

            time.sleep(1)
            limpiar_pantalla()
