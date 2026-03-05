from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto

'''
Supermercado que tiene clientes, proveedores y almacenes. 
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


class TipoProducto(Enum):
    FRESCO = auto()
    REFRIGERADO = auto()
    CONGELADO = auto()
    ENCONSERVA = auto()


@dataclass(frozen=True)
class Producto:
    '''
    Representa un producto del supermercado.
    Simplificación: Se 'decora' como inmutable (frozen=True) porque sus atributos 
    no deberían cambiar una vez creado.'''
    sku: str
    tipo: TipoProducto
    nombre: str
    precio: float


@dataclass
class Cesta:
    """Cesta de compra: sku -> cantidad."""
    lineas: Dict[str, int] = field(default_factory=dict)

    def anadir(self, sku: str, cantidad: int = 1) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad a añadir debe ser > 0")
        self.lineas[sku] = self.lineas.get(sku, 0) + cantidad

    def quitar(self, sku: str, cantidad: int = 1) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad a quitar debe ser > 0")
        if sku not in self.lineas:
            return
        self.lineas[sku] -= cantidad
        if self.lineas[sku] <= 0:
            del self.lineas[sku]

    def vaciar(self) -> None:
        self.lineas.clear()

    def esta_vacia(self) -> bool:
        return not self.lineas


# =========================
# Stock y almacenes
# =========================

@dataclass
class StockItem:
    producto: Producto
    cantidad: int
    umbral_reposicion: int
    objetivo_reposicion: int  # hasta cuánto queremos reponer (por ejemplo)

    def necesita_reposicion(self) -> bool:
        return self.cantidad < self.umbral_reposicion

    def cantidad_a_pedir(self) -> int:
        # Ejemplo: reponer hasta "objetivo_reposicion"
        return max(0, self.objetivo_reposicion - self.cantidad)


@dataclass
class Almacen:
    id_almacen: str
    inventario: Dict[str, StockItem] = field(default_factory=dict)  # sku -> StockItem

    def hay_existencias(self, sku: str, cantidad: int) -> bool:
        item = self.inventario.get(sku)
        return item is not None and item.cantidad >= cantidad

    def reservar_disponible(self, cesta: Cesta) -> bool:
        """Chequeo simple: ¿hay stock para todas las líneas?"""
        for sku, qty in cesta.lineas.items():
            if not self.hay_existencias(sku, qty):
                return False
        return True

    def descontar(self, sku: str, cantidad: int) -> None:
        if not self.hay_existencias(sku, cantidad):
            raise RuntimeError(f"Stock insuficiente para sku={sku}")
        self.inventario[sku].cantidad -= cantidad

    def reposiciones_necesarias(self) -> List[Tuple[str, int]]:
        """
        Devuelve lista de (sku, cantidad_a_pedir) para los items
        que han caído por debajo del umbral.
        """
        pedidos: List[Tuple[str, int]] = []
        for sku, item in self.inventario.items():
            if item.necesita_reposicion():
                qty = item.cantidad_a_pedir()
                if qty > 0:
                    pedidos.append((sku, qty))
        return pedidos

    def recibir_reposicion(self, sku: str, cantidad: int) -> None:
        if cantidad <= 0:
            return
        if sku not in self.inventario:
            raise KeyError(f"SKU {sku} no existe en este almacén")
        self.inventario[sku].cantidad += cantidad


# =========================
# Proveedores y pedidos
# =========================

class EstadoPedido(Enum):
    CREADO = auto()
    ENVIADO = auto()
    RECIBIDO = auto()
    CANCELADO = auto()


@dataclass
class PedidoProveedor:
    proveedor_id: str
    almacen_id: str
    lineas: List[Tuple[str, int]]  # [(sku, qty), ...]
    estado: EstadoPedido = EstadoPedido.CREADO

    def enviar(self) -> None:
        if self.estado != EstadoPedido.CREADO:
            return
        self.estado = EstadoPedido.ENVIADO

    def marcar_recibido(self) -> None:
        if self.estado != EstadoPedido.ENVIADO:
            return
        self.estado = EstadoPedido.RECIBIDO


@dataclass
class Proveedor:
    id_proveedor: str
    nombre: str
    # catálogo simple: sku -> precio_compra (no se usa mucho aquí)
    catalogo: Dict[str, float] = field(default_factory=dict)

    def crear_pedido(self, almacen_id: str, lineas: List[Tuple[str, int]]) -> PedidoProveedor:
        # En un sistema real: validar catálogo, plazos, etc.
        return PedidoProveedor(self.id_proveedor, almacen_id, lineas)


# =========================
# Clientes y pago
# =========================

@dataclass
class Cliente:
    id_cliente: str
    nombre: str
    metodo_pago: str  # "tarjeta", "bizum", etc. (simplificado)

    def iniciar_compra(self) -> Cesta:
        return Cesta()


@dataclass
class ResultadoPago:
    ok: bool
    motivo: Optional[str] = None
    id_transaccion: Optional[str] = None


class PasarelaPago:
    """Interfaz/servicio simplificado. Aquí se simula el pago."""
    def cobrar(self, cliente: Cliente, importe: float) -> ResultadoPago:
        if importe <= 0:
            return ResultadoPago(ok=False, motivo="Importe inválido")

        # Simulación: falla si el método de pago es "rechazado"
        if cliente.metodo_pago.lower() == "rechazado":
            return ResultadoPago(ok=False, motivo="Pago rechazado por la pasarela")

        return ResultadoPago(ok=True, id_transaccion="TX-FAKE-0001")


# =========================
# Supermercado (orquestación)
# =========================

class Supermercado:
    def __init__(self, nombre: str, pasarela_pago: PasarelaPago) -> None:
        self.nombre = nombre
        self._pasarela_pago = pasarela_pago

        self._clientes: Dict[str, Cliente] = {}
        self._proveedores: Dict[str, Proveedor] = {}
        self._almacenes: Dict[str, Almacen] = {}

        # Mapeo simple de surtido: sku -> lista de almacenes donde se busca
        # (en un sistema real: optimización por cercanía, coste, etc.)
        self._ruteo_stock: Dict[str, List[str]] = {}

    # ---- altas ----
    def alta_cliente(self, cliente: Cliente) -> None:
        self._clientes[cliente.id_cliente] = cliente

    def alta_proveedor(self, proveedor: Proveedor) -> None:
        self._proveedores[proveedor.id_proveedor] = proveedor

    def alta_almacen(self, almacen: Almacen) -> None:
        self._almacenes[almacen.id_almacen] = almacen
        # Recalcular ruteo para los SKUs que tenga este almacén
        for sku in almacen.inventario.keys():
            self._ruteo_stock.setdefault(sku, [])
            if almacen.id_almacen not in self._ruteo_stock[sku]:
                self._ruteo_stock[sku].append(almacen.id_almacen)

    # ---- compra ----
    def confirmar_compra(self, id_cliente: str, cesta: Cesta) -> Tuple[bool, str]:
        """
        Flujo:
        1) Validar cliente y cesta
        2) Elegir almacén que pueda servir TODO
        3) Calcular total
        4) Cobrar
        5) Descontar stock
        6) Si cae bajo umbral -> generar pedido a proveedor
        """
        if id_cliente not in self._clientes:
            return False, "Cliente no registrado"
        if cesta.esta_vacia():
            return False, "La cesta está vacía"

        cliente = self._clientes[id_cliente]

        almacen = self._seleccionar_almacen_para_cesta(cesta)
        if almacen is None:
            return False, "No hay existencias suficientes para completar la compra"

        total = self._calcular_total(cesta, almacen)
        pago = self._pasarela_pago.cobrar(cliente, total)
        if not pago.ok:
            return False, f"Pago fallido: {pago.motivo}"

        # Pago OK -> descontar stock
        for sku, qty in cesta.lineas.items():
            almacen.descontar(sku, qty)

        # Reposición si procede
        self._gestionar_reposicion(almacen)

        cesta.vaciar()
        return True, f"Compra confirmada. Total={total:.2f}€, transacción={pago.id_transaccion}"

    def _seleccionar_almacen_para_cesta(self, cesta: Cesta) -> Optional[Almacen]:
        """
        Estrategia simple: encontrar el primer almacén que pueda servir la cesta completa.
        (Alternativa: dividir por almacenes, backtracking, etc.)
        """
        candidatos = self._almacenes.values()
        for alm in candidatos:
            if alm.reservar_disponible(cesta):
                return alm
        return None

    def _calcular_total(self, cesta: Cesta, almacen: Almacen) -> float:
        total = 0.0
        for sku, qty in cesta.lineas.items():
            item = almacen.inventario.get(sku)
            if item is None:
                raise RuntimeError(f"SKU {sku} no existe en el almacén seleccionado")
            total += item.producto.precio * qty
        return total

    def _gestionar_reposicion(self, almacen: Almacen) -> None:
        """
        Estrategia docente: se hace pedido al "primer proveedor disponible"
        que tenga el SKU en su catálogo (si lo hay).
        """
        repos = almacen.reposiciones_necesarias()
        if not repos:
            return

        lineas_a_pedir: List[Tuple[str, int]] = []
        for sku, qty in repos:
            proveedor = self._buscar_proveedor_para_sku(sku)
            if proveedor is None:
                # En real: alertar, registrar incidencia, etc.
                continue
            lineas_a_pedir.append((sku, qty))

            pedido = proveedor.crear_pedido(almacen.id_almacen, [(sku, qty)])
            pedido.enviar()

            # Simulación de recepción inmediata:
            pedido.marcar_recibido()
            almacen.recibir_reposicion(sku, qty)

    def _buscar_proveedor_para_sku(self, sku: str) -> Optional[Proveedor]:
        for prov in self._proveedores.values():
            if sku in prov.catalogo:
                return prov
        return None


# =========================
# DEMO (uso docente)
# =========================

def demo() -> None:
    pasarela = PasarelaPago()
    market = Supermercado("SuperEjemplo", pasarela)

    # Productos
    leche = Producto("SKU-LECHE", "Leche entera 1L", 1.15)
    pan = Producto("SKU-PAN", "Pan barra", 0.85)

    # Almacén con umbrales
    almacen_central = Almacen(
        "ALM-CENTRAL",
        inventario={
            leche.sku: StockItem(leche, cantidad=5, umbral_reposicion=3, objetivo_reposicion=10),
            pan.sku: StockItem(pan, cantidad=20, umbral_reposicion=10, objetivo_reposicion=30),
        },
    )
    market.alta_almacen(almacen_central)

    # Proveedor
    proveedor = Proveedor(
        "PROV-01",
        "Lácteos y Pan S.A.",
        catalogo={leche.sku: 0.60, pan.sku: 0.30},
    )
    market.alta_proveedor(proveedor)

    # Cliente
    cliente = Cliente("CLI-01", "Ana", metodo_pago="tarjeta")
    market.alta_cliente(cliente)

    # Compra: iniciar -> cesta -> añadir/quitar -> confirmar
    cesta = cliente.iniciar_compra()
    cesta.anadir(leche.sku, 3)     # dejará la leche en 2 (por debajo del umbral=3) -> dispara reposición
    cesta.anadir(pan.sku, 2)
    cesta.quitar(pan.sku, 1)

    ok, msg = market.confirmar_compra(cliente.id_cliente, cesta)
    print(ok, msg)

    # Ver stock final (tras reposición simulada)
    print("Stock leche:", almacen_central.inventario[leche.sku].cantidad)
    print("Stock pan:", almacen_central.inventario[pan.sku].cantidad)


if __name__ == "__main__":
    demo()