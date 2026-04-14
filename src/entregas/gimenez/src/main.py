from flota import (
    Ubicacion, ClaseNave, EstacionEspacial, NaveEstelar, CazaEstelar,
    Repuesto, Almacen, Comandante, OperarioAlmacen, ExcepcionStockInsuficiente
)

def main():
    print("="*50)
    print("SISTEMA DE GESTIÓN MECÁNICA - MiImperio")
    print("="*50 + "\n")

    #########################################################################################################################
    
    # 1. Instanciación de la Flota Espacial
    print("[1] INSTANCIANDO LA FLOTA ESPACIAL...")
    
    # Creamos una estación espacial con ubicación en Endor, tripulación y pasaje
    estrella_muerte = EstacionEspacial(
        identificador_combate="DS-1", 
        clave_transmision_cifrada=12345, 
        nombre="Estrella de la Muerte", 
        tripulacion=342953, 
        pasaje=843342, 
        ubicacion=Ubicacion.ENDOR
    )
    
    # Creamos una nave estelar de clase Ejecutor con tripulación y pasaje
    destructor = NaveEstelar(
        identificador_combate="EXE-01", 
        clave_transmision_cifrada=98765, 
        nombre="Ejecutor Supremo", 
        tripulacion=279144, 
        pasaje=38000, 
        clase=ClaseNave.EJECUTOR
    )
    
    # Creamos un caza estelar con dotación de 1 piloto, sin tripulación ni pasaje
    caza_tie = CazaEstelar(
        identificador_combate="TIE-LN-1", 
        clave_transmision_cifrada=11111, 
        nombre="Caza TIE Alfa", 
        dotacion=1
    )

    print(f"\t-> Creada Estación: {estrella_muerte.nombre} en {estrella_muerte.ubicacion.value}")
    print(f"\t-> Creada Nave Estelar: {destructor.nombre} clase {destructor.clase.value}")
    print(f"\t-> Creado Caza: {caza_tie.nombre} con dotación de {caza_tie.dotacion}")

    #########################################################################################################################
    
    # 2. Instanciación de Inventario y Personal
    print("\n[2] CONFIGURANDO ALMACENES Y PERSONAL...")
    
    #Creamos un almacén central para la flota
    almacen_central = Almacen(
        nombre="Almacén Imperial Central",
        localizacion="Coruscant"
    )
    print(f"\t-> Almacén '{almacen_central.nombre}' ubicado en {almacen_central.localizacion} listo para operar.")
    
    # Creamos un repuesto para el almacén
    motor_ionico = Repuesto(
        nombre="Motor Iónico TIE", 
        proveedor="Sienar Fleet Systems", 
        cantidad_disponible=50, 
        precio=2500.50
    )
    
    # Creamos otro repuesto para el almacén
    panel_solar = Repuesto(
        nombre="Panel Solar TIE", 
        proveedor="Sienar Fleet Systems", 
        cantidad_disponible=10, 
        precio=800.00
    )
    
    # Instanciamos un operario de almacén que se encargará de gestionar el inventario
    operario = OperarioAlmacen(
        nombre="TK-421"
    )
    print(f"\t-> Operario '{operario.nombre}' listo para gestionar el inventario.")
    
    # Intanciamos un comandante que intentará adquirir repuestos
    comandante = Comandante(
        nombre="Darth Vader"
    )
    print(f"\t-> Comandante '{comandante.nombre}' listo para operar.")

    #########################################################################################################################

    # 3. Simulación: El operario abastece el almacén
    print("\n[3] OPERARIO ACTUALIZANDO INVENTARIO...")
    
    # El operario añade los repuestos al almacén, mostrando el resultado de cada acción
    operario.mantener_lista_repuestos(
        almacen=almacen_central,
        repuesto=motor_ionico,
        accion="añadir"
    )
    print(f"\t-> Repuesto '{motor_ionico.nombre}' añadido a {almacen_central.nombre} con stock inicial de {motor_ionico.get_cantidad_disponible()} unidades.")
    
    # El operario añade el segundo repuesto al almacén y se muestra el resultado
    operario.mantener_lista_repuestos(
        almacen=almacen_central,
        repuesto=panel_solar,
        accion="añadir"
    )
    print(f"\t-> Repuesto '{panel_solar.nombre}' añadido a {almacen_central.nombre} con stock inicial de {panel_solar.get_cantidad_disponible()} unidades.")

    #########################################################################################################################

    # 4. Simulación: Compras y control de Excepciones
    print("\n[4] COMANDANTE ADQUIRIENDO REPUESTOS...")
    
    # Intentamos comprar repuestos, manejando tanto el escenario de éxito como el de fallo
    try:
        
        # Escenario de Éxito (Hay 50 motores, pedimos 20)
        print(f"\t-> Intentando comprar 20 unidades de '{motor_ionico.nombre}'...", end="\n\t\t")
        # El comandante adquiere el repuesto, y se muestra el resultado de la operación
        comandante.adquirir_repuesto(
            almacen=almacen_central,
            repuesto=motor_ionico,
            cantidad=20
        )
        # Escenario de Fallo (Hay 10 paneles, pedimos 20)
        print(f"\t-> Intentando comprar 20 unidades de '{panel_solar.nombre}'...", end="\n\t\t")
        # El comandante intenta adquirir el repuesto, lo que debería generar una excepción por stock insuficiente
        comandante.adquirir_repuesto(
            almacen=almacen_central,
            repuesto=panel_solar,
            cantidad=20
        )
    
    # En caso de error de stock insuficiente o valor inválido, se captura la excepción y se muestra el mensaje correspondiente
    except ExcepcionStockInsuficiente as error_stock:
        print(f"Fracaso: {error_stock}")
        
    # Captura de cualquier otro error relacionado con valores inválidos (como cantidades negativas)
    except ValueError as error_valor:
        print(f"Error: {error_valor}")
    
    #########################################################################################################################

    print("\n" + "="*50)
    print("FIN DE LA SIMULACIÓN")
    print("="*50)

if __name__ == "__main__":
    main()