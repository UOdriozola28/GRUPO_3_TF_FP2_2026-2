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
    def __init__(self, numero, mesa):
        self.__numero = numero
        self.__mesa = mesa
        self.__estado = "Listo"
        self.__detalles = []

    def agregar_detalle(self, producto, cantidad, precio_unitario):
        self.__detalles.append(DetallePedido(producto, cantidad, precio_unitario))

    def obtener_numero(self):
        return self.__numero

    def obtener_mesa(self):
        return self.__mesa

    def obtener_estado(self):
        return self.__estado

    def obtener_detalles(self):
        return self.__detalles

    def calcular_subtotal(self):
        return sum(detalle.calcular_subtotal() for detalle in self.__detalles)

    def calcular_recargo(self):
        return self.calcular_subtotal() * 0.10

    def calcular_total(self):
        return self.calcular_subtotal() + self.calcular_recargo()

    def pagar(self):
        self.__estado = "Pagado"


class RestaurantePreview:
    def __init__(self):
        self.__cajero = Cajero("EMP021", "Carlos Mendoza")
        self.__mesa = Mesa(7)
        self.__pedido = Pedido("PED-000001", self.__mesa)
        self.__pedido.agregar_detalle(Producto("Maki acevichado"), 2, 28.00)
        self.__pedido.agregar_detalle(Producto("Gyoza de cerdo"), 1, 18.00)
        self.__pedido.agregar_detalle(Producto("Ramen tonkotsu"), 1, 26.00)
        self.__pedido.agregar_detalle(Producto("Te verde frio 1 L"), 1, 12.00)
        self.__comprobantes = []
        self.__numero_boleta = 0
        self.__numero_factura = 0

    def buscar_pedido_por_numero(self, numero):
        if self.__pedido.obtener_numero() == numero:
            return self.__pedido
        return None

    def buscar_pedido_por_mesa(self, numero):
        if self.__mesa.obtener_numero() == numero:
            return self.__pedido
        return None

    def buscar_empleado(self, codigo):
        if self.__cajero.obtener_codigo() == codigo:
            return self.__cajero
        return None

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
        pedido.obtener_mesa().liberar()

    def listar_comprobantes(self):
        return self.__comprobantes


def main():
    restaurante = RestaurantePreview()
    print("\nPREVIEW DE FACTURACION - SAKURAMAKI")
    print("Pedido disponible: PED-000001 | Mesa: 7 | Cajero: EMP021")
    facturacion.menu(restaurante)
    print("\nFin de la preview.")


if __name__ == "__main__":
    main()
