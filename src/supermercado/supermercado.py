'''
* Supermercado que tiene clientes, proveedores y almacenes. 

* Los clientes compran productos y los almacenes proporcionan productos. 

* Los productos puedeb ser de distintos tipos (frescos, refrigerados, congelados, en conserva, etc.) 
  y cada tipo tiene sus propias características.

* Clientes y proveedores se dan de alta. 

* Cuando los clientes inician una compra se les proporciona una cesta vacía 
  a la que van añadiendo o quitando productos. 

* Cuando la cesta tiene los productos deseados los clientes confirman la compra. 

* Cuando se confirma la compra el supermercado comprueba si hay existencias 
  en los almacenes.

* Si las hay solicita el pago al cliente, sino se eleva una excepción. 

* Si el pago se realiza correctamente se actualizan la compra se da por realizada y 
  se actualizan las existencias del almacén correspondiente. 

* Si como resultado de la compra las existencias de un producto bajan por debajo 
  de un cierto umbral se hace un pedido a un proveedor para reponer existencias.
'''


from enum import Enum


class TipoProducto(Enum):
    CONGELADO = 1
    FRESCO = 2
    ENCONSERVA = 3
    REFRIGERADO = 4


class Producto:
    def __init__(self, sku, nombre, precio, tipo_producto):
        self.sku = sku
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo_producto  # TipoProducto


class Cesta:
    def __init__(self):
        # lineas: sku -> cantidad
        self.lineas = {}

    def anadir(self, sku, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        if sku not in self.lineas:
            self.lineas[sku] = 0
        self.lineas[sku] += cantidad

    def quitar(self, sku, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        if sku not in self.lineas:
            return
        self.lineas[sku] -= cantidad
        if self.lineas[sku] <= 0:
            del self.lineas[sku]

    def vacia(self):
        return len(self.lineas) == 0

    def vaciar(self):
        self.lineas = {}



class Entidad:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class Cliente(Entidad):
    def __init__(self, id, nombre, metodo_pago):
        super().__init__(id, nombre)
        self.metodo_pago = metodo_pago

class Proveedor(Entidad):
    def __init__(self, id, nombre, catalogo_skus):
        super().__init__(id, nombre)
        self.catalogo_skus = set(catalogo_skus)

    def puede_servir(self, sku):
        return sku in self.catalogo_skus

    def servir_pedido(self, pedido):
        # Simulación: siempre sirve
        return True


class PedidoProveedor:
    def __init__(self, proveedor, almacen, lineas):
        self.proveedor = proveedor
        self.almacen = almacen
        self.lineas = lineas  # [(sku, cantidad), ...]
        self.estado = "CREADO"

    def enviar(self):
        self.estado = "ENVIADO"

    def recibir(self):
        self.estado = "RECIBIDO"


class Almacen:
    def __init__(self, id_almacen):
        self.id_almacen = id_almacen
        self.productos = {}   # sku -> Producto
        self.stock = {}       # sku -> cantidad
        self.umbral = {}      # sku -> umbral reposición
        self.objetivo = {}    # sku -> objetivo reposición

    def alta_producto(self, producto, cantidad_inicial, umbral_reposicion, objetivo_reposicion):
        self.productos[producto.sku] = producto
        self.stock[producto.sku] = cantidad_inicial
        self.umbral[producto.sku] = umbral_reposicion
        self.objetivo[producto.sku] = objetivo_reposicion

    def hay_existencias(self, sku, cantidad):
        return sku in self.stock and self.stock[sku] >= cantidad

    def puede_servir_cesta(self, cesta):
        for sku, qty in cesta.lineas.items():
            if not self.hay_existencias(sku, qty):
                return False
        return True

    def total_cesta(self, cesta):
        total = 0.0
        for sku, qty in cesta.lineas.items():
            total += self.productos[sku].precio * qty
        return total

    def descontar_cesta(self, cesta):
        for sku, qty in cesta.lineas.items():
            if not self.hay_existencias(sku, qty):
                raise RuntimeError("Stock insuficiente durante el descuento")
            self.stock[sku] -= qty

    def reposiciones_necesarias(self):
        pedidos = []
        for sku in self.stock:
            if self.stock[sku] < self.umbral[sku]:
                cantidad_a_pedir = self.objetivo[sku] - self.stock[sku]
                if cantidad_a_pedir > 0:
                    pedidos.append((sku, cantidad_a_pedir))
        return pedidos

    def recibir_reposicion(self, sku, cantidad):
        if sku not in self.stock:
            raise KeyError("SKU no existe en el almacén")
        self.stock[sku] += cantidad


class PasarelaPago:
    def cobrar(self, cliente, importe):
        if importe <= 0:
            return (False, "Importe inválido")
        if cliente.metodo_pago == "rechazado":
            return (False, "Pago rechazado")
        return (True, "TX-0001")


# =========================
# Supermercado (servicios)
# =========================

class Supermercado:
    def __init__(self, nombre, pasarela_pago):
        self.nombre = nombre
        self.pasarela_pago = pasarela_pago

        self.clientes = {}
        self.proveedores = {}
        self.almacenes = {}

        # NUEVO: compras activas
        # id_cliente -> Cesta
        self.compras_activas = {}

    def alta_cliente(self, cliente):
        self.clientes[cliente.id] = cliente

    def alta_proveedor(self, proveedor):
        self.proveedores[proveedor.id] = proveedor

    def alta_almacen(self, almacen):
        self.almacenes[almacen.id_almacen] = almacen

    def iniciar_compra(self, id_cliente):
        if id_cliente not in self.clientes:
            raise ValueError("Cliente no registrado")

        # si ya había una cesta activa, la reemplazamos.
        cesta = Cesta()
        self.compras_activas[id_cliente] = cesta
        return cesta

    def confirmar_compra(self, id_cliente):
        if id_cliente not in self.clientes:
            return (False, "Cliente no registrado")

        if id_cliente not in self.compras_activas:
            return (False, "No hay compra activa para este cliente")

        cesta = self.compras_activas[id_cliente]
        if cesta.vacia():
            return (False, "Cesta vacía")

        cliente = self.clientes[id_cliente]

        almacen = self._seleccionar_almacen(cesta)
        if almacen is None:
            return (False, "No hay existencias suficientes")

        total = almacen.total_cesta(cesta)
        ok, info = self.pasarela_pago.cobrar(cliente, total)
        if not ok:
            return (False, "Pago fallido: " + info)

        almacen.descontar_cesta(cesta)
        self._reponer_si_necesario(almacen)

        cesta.vaciar()
        # cerramos la compra activa
        del self.compras_activas[id_cliente]

        return (True, "Compra OK. Total=%.2f€, transacción=%s" % (total, info))

    def _seleccionar_almacen(self, cesta):
        for almacen in self.almacenes.values():
            if almacen.puede_servir_cesta(cesta):
                return almacen
        return None

    def _reponer_si_necesario(self, almacen):
        repos = almacen.reposiciones_necesarias()
        if len(repos) == 0:
            return

        for sku, cantidad in repos:
            proveedor = self._buscar_proveedor(sku)
            if proveedor is None:
                continue

            pedido = PedidoProveedor(proveedor, almacen, [(sku, cantidad)])
            pedido.enviar()

            servido = proveedor.servir_pedido(pedido)
            if servido:
                pedido.recibir()
                almacen.recibir_reposicion(sku, cantidad)

    def _buscar_proveedor(self, sku):
        for prov in self.proveedores.values():
            if prov.puede_servir(sku):
                return prov
        return None


# =========================
# DEMO
# =========================

def demo():
    pasarela = PasarelaPago()
    market = Supermercado("SuperEjemplo", pasarela)

    # Productos con TipoProducto
    leche = Producto("SKU-LECHE", "Leche entera 1L", 1.15, TipoProducto.FRESCO)
    guisantes = Producto("SKU-GUIS", "Guisantes congelados", 1.60, TipoProducto.CONGELADO)
    atun = Producto("SKU-ATUN", "Atún en lata", 1.20, TipoProducto.ENCONSERVA)

    # Almacén
    a1 = Almacen("ALM-1")
    a1.alta_producto(leche, cantidad_inicial=5, umbral_reposicion=3, objetivo_reposicion=10)
    a1.alta_producto(guisantes, cantidad_inicial=4, umbral_reposicion=2, objetivo_reposicion=8)
    a1.alta_producto(atun, cantidad_inicial=20, umbral_reposicion=10, objetivo_reposicion=30)
    market.alta_almacen(a1)

    # Proveedor
    prov1 = Proveedor("PROV-1", "Proveedor Uno", catalogo_skus=[leche.sku, guisantes.sku, atun.sku])
    market.alta_proveedor(prov1)

    # Cliente
    c1 = Cliente("CLI-1", "Ana", metodo_pago="tarjeta")
    market.alta_cliente(c1)

    # (1) iniciar_compra como servicio del supermercado
    cesta = market.iniciar_compra(c1.id)
    cesta.anadir(leche.sku, 3)      # dejará leche en 2 -> repone
    cesta.anadir(guisantes.sku, 1)
    cesta.anadir(atun.sku, 2)
    cesta.quitar(atun.sku, 1)

    ok, msg = market.confirmar_compra(c1.id)
    print(ok, msg)

    print("Stock leche:", a1.stock[leche.sku])
    print("Stock guisantes:", a1.stock[guisantes.sku])
    print("Stock atún:", a1.stock[atun.sku])


if __name__ == "__main__":
    demo()