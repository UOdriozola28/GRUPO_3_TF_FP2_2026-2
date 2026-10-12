from datetime import datetime

RECARGO_AL_CONSUMO = 0.10

class DetallePedido:

    def __init__(self, producto, cantidad):
        self.__producto = producto
        self.__cantidad = cantidad
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
        return self.__detalles

    def obtener_fecha_hora(self):
        return self.__fecha_hora

    def agregar_detalle(self, producto, cantidad):
        if self.esta_pagado():
            raise ValueError("No se puede modificar un pedido ya pagado.")
        detalle = DetallePedido(producto, cantidad)
        self.__detalles.append(detalle)

    def quitar_detalle(self, indice):
        if self.esta_pagado():
            raise ValueError("No se puede modificar un pedido ya pagado.")
        if indice < 0 or indice >= len(self.__detalles):
            raise IndexError("La linea indicada no existe en el pedido.")
        self.__detalles.pop(indice)

    def calcular_subtotal(self):
        total = 0.0
        for detalle in self.__detalles:
            total = total + detalle.calcular_subtotal()
        return total

    def calcular_recargo(self):
        if self.__canal == "Salon":
            return self.calcular_subtotal() * RECARGO_AL_CONSUMO
        else:
            return 0.0

    def calcular_total(self):
        return self.calcular_subtotal() + self.calcular_recargo()

    def cambiar_estado(self, nuevo):
        self.__estado = nuevo

    def esta_pagado(self):
        if self.__estado == "Pagado":
            return True
        else:
            return False

    def contar_items(self):
        total = 0
        for detalle in self.__detalles:
            total = total + detalle.obtener_cantidad()
        return total
