"""Preview sencilla del modulo de facturacion.

Ejecutar con: python3 main.py
"""

from modelo.comprobante import Boleta, Factura
from modulos import facturacion


class Producto:
    def __init__(self, nombre):
        self.__nombre = nombre

    def obtener_nombre(self):
        return self.__nombre


class DetallePedido:
    def __init__(self, producto, cantidad, precio_unitario):
        self.__producto = producto
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario

    def obtener_producto(self):
        return self.__producto

    def obtener_cantidad(self):
        return self.__cantidad

    def calcular_subtotal(self):
        return self.__cantidad * self.__precio_unitario


class Mesa:
    def __init__(self, numero):
        self.__numero = numero
        self.__libre = False

    def obtener_numero(self):
        return self.__numero

    def liberar(self):
        self.__libre = True


class Cajero:
    def __init__(self, codigo, nombres):
        self.__codigo = codigo
        self.__nombres = nombres

    def obtener_codigo(self):
        return self.__codigo

    def obtener_nombres(self):
        return self.__nombres

    def obtener_tipo(self):
        return "Cajero"


class Pedido:
    def __init__(self, numero, canal, mesa=None):
        self.__numero = numero
        self.__canal = canal
        self.__mesa = mesa
        self.__estado = "Listo"
        self.__detalles = []

    def agregar_detalle(self, producto, cantidad, precio_unitario):
        self.__detalles.append(DetallePedido(producto, cantidad, precio_unitario))

    def obtener_numero(self):
        return self.__numero

    def obtener_mesa(self):
        return self.__mesa

    def obtener_canal(self):
        return self.__canal

    def obtener_estado(self):
        return self.__estado

    def obtener_detalles(self):
        return self.__detalles

    def calcular_subtotal(self):
        return sum(detalle.calcular_subtotal() for detalle in self.__detalles)

    def calcular_recargo(self):
        if self.__canal == "Salon":
            return self.calcular_subtotal() * 0.10
        return 0.0

    def calcular_total(self):
        return self.calcular_subtotal() + self.calcular_recargo()

    def pagar(self):
        self.__estado = "Pagado"


class RestaurantePreview:
    def __init__(self):
        self.__cajeros = [
            Cajero("EMP021", "Carlos Mendoza"),
            Cajero("EMP022", "Lucia Fernandez"),
        ]

        mesa_7 = Mesa(7)
        mesa_12 = Mesa(12)

        pedido_1 = Pedido("PED-000001", "Salon", mesa_7)
        pedido_1.agregar_detalle(Producto("Maki acevichado"), 2, 28.00)
        pedido_1.agregar_detalle(Producto("Gyoza de cerdo"), 1, 18.00)
        pedido_1.agregar_detalle(Producto("Ramen tonkotsu"), 1, 26.00)
        pedido_1.agregar_detalle(Producto("Te verde frio 1 L"), 1, 12.00)

        pedido_2 = Pedido("PED-000002", "Salon", mesa_12)
        pedido_2.agregar_detalle(Producto("Combo Sakura"), 1, 45.00)
        pedido_2.agregar_detalle(Producto("Gaseosa personal"), 2, 6.00)

        pedido_3 = Pedido("PED-000003", "Delivery")
        pedido_3.agregar_detalle(Producto("Ramen tonkotsu"), 2, 26.00)
        pedido_3.agregar_detalle(Producto("Te verde frio 1 L"), 1, 12.00)

        self.__pedidos = [pedido_1, pedido_2, pedido_3]
        self.__comprobantes = []
        self.__numero_boleta = 0
        self.__numero_factura = 0

    def buscar_pedido_por_numero(self, numero):
        for pedido in self.__pedidos:
            if pedido.obtener_numero() == numero:
                return pedido
        return None

    def buscar_pedido_por_mesa(self, numero):
        for pedido in self.__pedidos:
            mesa = pedido.obtener_mesa()
            if mesa is not None and mesa.obtener_numero() == numero:
                return pedido
        return None

    def buscar_empleado(self, codigo):
        for cajero in self.__cajeros:
            if cajero.obtener_codigo() == codigo:
                return cajero
        return None

    def listar_pedidos(self):
        return self.__pedidos

    def listar_cajeros(self):
        return self.__cajeros

    def emitir_boleta(self, pedido, medio_pago, dni, nombre):
        self.__numero_boleta += 1
        comprobante = Boleta(self.__numero_boleta, pedido, medio_pago, dni, nombre)
        self.__cerrar_pedido(pedido)
        self.__comprobantes.append(comprobante)
        return comprobante

    def emitir_factura(self, pedido, medio_pago, ruc, razon_social):
        self.__numero_factura += 1
        comprobante = Factura(
            self.__numero_factura, pedido, medio_pago, ruc, razon_social
        )
        self.__cerrar_pedido(pedido)
        self.__comprobantes.append(comprobante)
        return comprobante

    def __cerrar_pedido(self, pedido):
        pedido.pagar()
        if pedido.obtener_mesa() is not None:
            pedido.obtener_mesa().liberar()

    def listar_comprobantes(self):
        return self.__comprobantes


def main():
    restaurante = RestaurantePreview()
    print("\nPREVIEW DE FACTURACION - SAKURAMAKI")
    print("\nDATOS PRECARGADOS")
    print("Cajeros:")
    for cajero in restaurante.listar_cajeros():
        print("  %s - %s" % (cajero.obtener_codigo(), cajero.obtener_nombres()))
    print("Pedidos listos:")
    for pedido in restaurante.listar_pedidos():
        mesa = "-"
        if pedido.obtener_mesa() is not None:
            mesa = str(pedido.obtener_mesa().obtener_numero())
        print("  %s | %-8s | Mesa: %-2s | Total: S/ %.2f" % (
            pedido.obtener_numero(), pedido.obtener_canal(), mesa,
            pedido.calcular_total(),
        ))
    facturacion.menu(restaurante)
    print("\nFin de la preview.")


if __name__ == "__main__":
    main()
