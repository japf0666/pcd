from enumeraciones import UbicacionEstacion, ClaseNaveEstelar
from dominio import EstacionEspacial, NaveEstelar, CazaEstelar, Almacen, Repuesto
from usuarios import Comandante, OperarioAlmacen
from sistema import MiImperio
from excepciones import MiImperioError


def imprimir_catalogo_filtrado(comandante: Comandante, almacen: Almacen) -> None:
    print(f"\nRepuestos disponibles para la nave '{comandante.nave.nombre}' en {almacen.nombre}:")
    
    disponibles: list[Repuesto] = []
    for repuesto in almacen.consultar_repuestos(comandante):
        if comandante.nave.admite_repuesto(repuesto.nombre):
            disponibles.append(repuesto)

    if not disponibles:
        print("  No hay repuestos compatibles.")
        return
    
    for repuesto in disponibles:
        print(f"  - {repuesto}")


def demo() -> None:
    print("=== DEMO MiImperio con clases abstractas ===")

    sistema = MiImperio()

    estacion = EstacionEspacial(
        nombre="Estrella de la Muerte II",
        catalogo_repuestos=["Escudo deflector", "Módulo de energía", "Panel térmico"],
        tripulacion=250000,
        pasaje=75000,
        ubicacion=UbicacionEstacion.ENDOR,
    )

    destructor = NaveEstelar(
        nombre="Executor",
        catalogo_repuestos=["Motor iónico", "Escudo deflector", "Cañón turbo láser"],
        tripulacion=280000,
        pasaje=38000,
        clase_nave=ClaseNaveEstelar.EJECUTOR,
        identificador_combate="NE-001",
        clave_transmision=987654,
    )

    caza = CazaEstelar(
        nombre="TIE Avanzado",
        catalogo_repuestos=["Motor iónico", "Panel solar", "Sistema de puntería"],
        dotacion=1,
        identificador_combate="CE-101",
        clave_transmision=123456,
    )

    sistema.registrar_nave(estacion)
    sistema.registrar_nave(destructor)
    sistema.registrar_nave(caza)

    print("\n--- Naves registradas ---")
    for nave in sistema.listar_naves():
        print(nave.descripcion())

    almacen_central = Almacen("Almacén Central", "Endor")
    sistema.registrar_almacen(almacen_central)

    operario = OperarioAlmacen("TK-421")

    almacen_central.alta_operario(operario)
    almacen_central.alta_repuesto(operario, Repuesto("Escudo deflector", "Kuat Systems", 10, 5000))
    almacen_central.alta_repuesto(operario, Repuesto("Motor iónico", "Sienar Fleet", 6, 3500))
    almacen_central.alta_repuesto(operario, Repuesto("Panel solar", "Sienar Fleet", 15, 1200))
    almacen_central.alta_repuesto(operario, Repuesto("Sistema de puntería", "BlasTech", 4, 2200))

    print("\n--- Repuestos en almacén ---")
    for repuesto in almacen_central.consultar_repuestos(operario):
        print(repuesto)

    comandante_executor = Comandante("Darth Vader", destructor)
    almacen_central.alta_comandante(comandante_executor)
    comandante_tie = Comandante("Maarek Stele", caza)
    almacen_central.alta_comandante(comandante_tie)

    imprimir_catalogo_filtrado(comandante_executor, almacen_central)
    imprimir_catalogo_filtrado(comandante_tie, almacen_central)

    print("\n--- Compra correcta ---")
    try:
        mensaje = almacen_central.solicitar_repuesto(comandante_executor, "Motor iónico", 2)
        print(mensaje)
    except MiImperioError as e:
        print("Error controlado:", e)

    print("\n--- Error: repuesto no autorizado para la nave ---")
    try:
        mensaje = almacen_central.solicitar_repuesto(comandante_executor, "Panel solar", 1)
        print(mensaje)
    except MiImperioError as e:
        print("Error controlado:", e)

    print("\n--- Error: stock insuficiente ---")
    try:
        mensaje = almacen_central.solicitar_repuesto(comandante_tie, "Sistema de puntería", 10)
        print(mensaje)
    except MiImperioError as e:
        print("Error controlado:", e)

    print("\n--- Reposición de stock ---")
    try:
        almacen_central.reponer_stock(operario, "Sistema de puntería", 10)
        print("Stock repuesto correctamente.")
        print(almacen_central.buscar_repuesto(operario, "Sistema de puntería"))
    except MiImperioError as e:
        print("Error controlado:", e)

    print("\n--- Compra tras reposición ---")
    try:
        mensaje = almacen_central.solicitar_repuesto(comandante_tie, "Sistema de puntería", 5)
        print(mensaje)
    except MiImperioError as e:
        print("Error controlado:", e)

    print("\n--- Mensajes cifrados ---")
    print(destructor.transmitir_mensaje_cifrado("Objetivo fijado"))
    print(caza.transmitir_mensaje_cifrado("Ataque en formación"))

    print("\n=== FIN DEMO ===")


if __name__ == "__main__":
    demo()