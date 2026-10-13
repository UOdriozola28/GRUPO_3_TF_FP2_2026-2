from modelo.pedido import Pedido
from modelo.comprobante import Boleta, Factura

class Restaurante:

    def __init__(self, razon_social, ruc):
        self.__razon_social = razon_social
        self.__ruc = ruc
        self.__productos = []
        self.__empleados = []
        self.__mesas = []
        self.__pedidos = []
        self.__comprobantes = []
        self.__contador_pedidos = 0
        self.__contador_boletas = 0
        self.__contador_facturas = 0

    def obtener_razon_social(self):
        return self.__razon_social

    def obtener_ruc(self):
        return self.__ruc

    def registrar_producto(self, producto):
        if self.buscar_producto(producto.obtener_codigo()) is not None:
            raise ValueError("Ya existe un producto con el codigo " + producto.obtener_codigo())
        self.__productos.append(producto)

    def listar_productos(self):
        return self.__productos

    def buscar_producto(self, codigo):
        for producto in self.__productos:
            if producto.obtener_codigo() == codigo:
                return producto
        return None

    def registrar_empleado(self, empleado):
        if self.buscar_empleado(empleado.obtener_codigo()) is not None:
            raise ValueError("Ya existe un empleado con el codigo " + empleado.obtener_codigo())
        self.__empleados.append(empleado)

    def listar_empleados(self):
        return self.__empleados

    def buscar_empleado(self, codigo):
        for empleado in self.__empleados:
            if empleado.obtener_codigo() == codigo:
                return empleado
        return None

    def listar_mozos(self):
        mozos = []
        for empleado in self.__empleados:
            if empleado.obtener_tipo() == "Mozo":
                mozos.append(empleado)
        return mozos

    def registrar_mesa(self, mesa):
        self.__mesas.append(mesa)

    def listar_mesas(self):
        return self.__mesas

    def listar_mesas_libres(self):
        libres = []
        for mesa in self.__mesas:
            if mesa.esta_libre():
                libres.append(mesa)
        return libres

    def buscar_mesa(self, numero):
        for mesa in self.__mesas:
            if mesa.obtener_numero() == numero:
                return mesa
        return None

    def generar_numero_pedido(self):
        self.__contador_pedidos = self.__contador_pedidos + 1
        numero = str(self.__contador_pedidos)
        while len(numero) < 6:
            numero = "0" + numero
        return "PED-" + numero

    def registrar_pedido(self, canal, mesa, mozo):
        numero = self.generar_numero_pedido()
        pedido = Pedido(numero, canal, mesa, mozo)
        if mesa is not None:
            mesa.ocupar()
        self.__pedidos.append(pedido)
        return pedido

    def listar_pedidos(self):
        return self.__pedidos

    def buscar_pedido_por_numero(self, numero):
        for pedido in self.__pedidos:
            if pedido.obtener_numero() == numero:
                return pedido
        return None

    def buscar_pedido_por_mesa(self, numero_mesa):
        for pedido in self.__pedidos:
            mesa = pedido.obtener_mesa()
            if mesa is not None and mesa.obtener_numero() == numero_mesa:
                if not pedido.esta_pagado():
                    return pedido
        return None

    def emitir_boleta(self, pedido, medio_pago, dni, nombre):
        self.__contador_boletas = self.__contador_boletas + 1
        boleta = Boleta(self.__contador_boletas, pedido, medio_pago, dni, nombre)
        self.__comprobantes.append(boleta)
        self.cerrar_pedido(pedido)
        return boleta

    def emitir_factura(self, pedido, medio_pago, ruc, razon_social):
        self.__contador_facturas = self.__contador_facturas + 1
        factura = Factura(self.__contador_facturas, pedido, medio_pago, ruc, razon_social)
        if not factura.validar_ruc():
            self.__contador_facturas = self.__contador_facturas - 1
            raise ValueError("El RUC debe tener once digitos numericos.")
        self.__comprobantes.append(factura)
        self.cerrar_pedido(pedido)
        return factura

    def cerrar_pedido(self, pedido):
        pedido.cambiar_estado("Pagado")
        mesa = pedido.obtener_mesa()
        if mesa is not None:
            mesa.liberar()
        mozo = pedido.obtener_mozo()
        if mozo is not None:
            mozo.registrar_propina(pedido.calcular_subtotal())

    def listar_comprobantes(self):
        return self.__comprobantes
