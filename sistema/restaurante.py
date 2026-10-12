from modelo.comprobante import Boleta, Factura
from modelo.pedido import Pedido


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

    def registrar_producto(self, producto):
        if self.buscar_producto(producto.obtener_codigo()) is not None:
            raise ValueError("El codigo del producto ya esta registrado.")
        self.__productos.append(producto)

    def listar_productos(self):
        return list(self.__productos)

    def buscar_producto(self, codigo):
        return next((p for p in self.__productos if p.obtener_codigo() == codigo), None)

    def registrar_empleado(self, empleado):
        if self.buscar_empleado(empleado.obtener_codigo()) is not None:
            raise ValueError("El codigo del empleado ya esta registrado.")
        self.__empleados.append(empleado)

    def listar_empleados(self):
        return list(self.__empleados)

    def buscar_empleado(self, codigo):
        return next((e for e in self.__empleados if e.obtener_codigo() == codigo), None)

    def buscar_cajero_activo(self, codigo):
        empleado = self.buscar_empleado(codigo)
        if empleado is None:
            raise ValueError("El empleado %s no se encuentra registrado." % codigo)
        if not empleado.esta_activo():
            raise ValueError("El empleado %s no se encuentra activo." % codigo)
        if empleado.obtener_tipo() != "Cajero":
            raise ValueError("El empleado %s no tiene el rol Cajero." % codigo)
        return empleado

    def registrar_mesa(self, mesa):
        self.__mesas.append(mesa)

    def listar_mesas(self):
        return list(self.__mesas)

    def buscar_mesa(self, numero):
        return next((m for m in self.__mesas if m.obtener_numero() == numero), None)

    def generar_numero_pedido(self):
        self.__contador_pedidos += 1
        return "PED-%06d" % self.__contador_pedidos

    def registrar_pedido(self, canal, mesa, mozo):
        pedido = Pedido(self.generar_numero_pedido(), canal, mesa, mozo)
        if mesa is not None:
            if not mesa.esta_libre():
                raise ValueError("La mesa se encuentra ocupada.")
            mesa.ocupar()
        self.__pedidos.append(pedido)
        return pedido

    def listar_pedidos(self):
        return list(self.__pedidos)

    def buscar_pedido_por_numero(self, numero):
        return next((p for p in self.__pedidos if p.obtener_numero() == numero), None)

    def buscar_pedido_por_mesa(self, numero_mesa):
        for pedido in self.__pedidos:
            mesa = pedido.obtener_mesa()
            if mesa is not None and mesa.obtener_numero() == numero_mesa and not pedido.esta_pagado():
                return pedido
        return None

    def _validar_emision(self, pedido, cajero):
        if pedido not in self.__pedidos:
            raise ValueError("El pedido no pertenece al restaurante.")
        if not pedido.esta_listo():
            raise ValueError("Solo se puede facturar un pedido en estado Listo.")
        if not pedido.obtener_detalles():
            raise ValueError("El pedido no tiene productos registrados.")
        return self.buscar_cajero_activo(cajero.obtener_codigo())

    def emitir_boleta(self, pedido, medio_pago, cajero, dni="", nombre=""):
        cajero = self._validar_emision(pedido, cajero)
        if dni and (len(dni) != 8 or not dni.isdigit()):
            raise ValueError("El DNI debe tener ocho digitos numericos.")
        correlativo = self.__contador_boletas + 1
        boleta = Boleta(correlativo, pedido, medio_pago, cajero, dni, nombre)
        self.__contador_boletas = correlativo
        self.__comprobantes.append(boleta)
        self.cerrar_pedido(pedido)
        return boleta

    def emitir_factura(self, pedido, medio_pago, cajero, ruc, razon_social):
        cajero = self._validar_emision(pedido, cajero)
        correlativo = self.__contador_facturas + 1
        factura = Factura(correlativo, pedido, medio_pago, cajero, ruc, razon_social)
        self.__contador_facturas = correlativo
        self.__comprobantes.append(factura)
        self.cerrar_pedido(pedido)
        return factura

    def cerrar_pedido(self, pedido):
        pedido.cambiar_estado("Pagado")
        mesa = pedido.obtener_mesa()
        if mesa is not None:
            mesa.liberar()
        mozo = pedido.obtener_mozo()
        if mozo is not None and hasattr(mozo, "registrar_propina"):
            mozo.registrar_propina(pedido.calcular_subtotal())

    def listar_comprobantes(self):
        return list(self.__comprobantes)
