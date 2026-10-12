from datetime import datetime

RECARGO_AL_CONSUMO = 0.10
TRANSICIONES = {
    "Registrado": "En preparacion",
    "En preparacion": "Listo",
    "Listo": "Pagado",
}


class DetallePedido:
    def __init__(self, producto, cantidad, empleado=None):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self.__producto = producto
        self.__cantidad = cantidad
        self.__empleado = empleado
        self.__precio_unitario = producto.calcular_precio()

    def obtener_producto(self):
        return self.__producto

    def obtener_cantidad(self):
        return self.__cantidad

    def obtener_precio_unitario(self):
        return self.__precio_unitario

    def calcular_subtotal(self):
        return self.__precio_unitario * self.__cantidad


class Pedido:
    def __init__(self, numero, canal, mesa, mozo):
        self.__numero = numero
        self.__canal = canal
        self.__mesa = mesa
        self.__mozo = mozo
        self.__fecha_hora = datetime.now()
        self.__estado = "Registrado"
        self.__detalles = []

    def obtener_numero(self):
        return self.__numero

    def obtener_canal(self):
        return self.__canal

    def obtener_mesa(self):
        return self.__mesa

    def obtener_mozo(self):
        return self.__mozo

    def obtener_estado(self):
        return self.__estado

    def obtener_detalles(self):
        return list(self.__detalles)

    def obtener_fecha_hora(self):
        return self.__fecha_hora

    def agregar_detalle(self, producto, cantidad, empleado=None):
        if self.__estado == "Pagado":
            raise ValueError("No se puede modificar un pedido pagado.")
        self.__detalles.append(DetallePedido(producto, cantidad, empleado))

    def calcular_subtotal(self):
        return sum(detalle.calcular_subtotal() for detalle in self.__detalles)

    def calcular_recargo(self):
        return self.calcular_subtotal() * RECARGO_AL_CONSUMO if self.__canal == "Salon" else 0.0

    def calcular_total(self):
        return self.calcular_subtotal() + self.calcular_recargo()

    def cambiar_estado(self, nuevo_estado):
        esperado = TRANSICIONES.get(self.__estado)
        if nuevo_estado != esperado:
            raise ValueError("Cambio de estado no permitido: %s a %s." % (self.__estado, nuevo_estado))
        self.__estado = nuevo_estado

    def esta_pagado(self):
        return self.__estado == "Pagado"

    def esta_listo(self):
        return self.__estado == "Listo"

    def contar_items(self):
        return sum(detalle.obtener_cantidad() for detalle in self.__detalles)
