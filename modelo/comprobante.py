from abc import ABC, abstractmethod
from datetime import datetime

from utiles.formato import recortar

IGV = 0.18
ANCHO = 64


class Comprobante(ABC):

    def __init__(self, serie, correlativo, pedido, medio_pago):
        if pedido.esta_pagado():
            raise ValueError("El pedido ya fue pagado.")
        if len(pedido.obtener_detalles()) == 0:
            raise ValueError("El pedido no tiene productos registrados.")
        self.__serie = serie
        self.__correlativo = correlativo
        self.__pedido = pedido
        self.__medio_pago = medio_pago
        self.__fecha_emision = datetime.now()

    def obtener_numero_completo(self):
        correlativo = str(self.__correlativo).rjust(6, "0")
        return f"{self.__serie}-{correlativo}"

    def obtener_pedido(self):
        return self.__pedido

    def obtener_medio_pago(self):
        return self.__medio_pago

    def obtener_fecha_emision(self):
        return self.__fecha_emision

    def calcular_total(self):
        return self.__pedido.calcular_total()

    def _lineas_detalle(self):
        lineas = ["CANT  DESCRIPCION".ljust(52) + "IMPORTE", "-" * ANCHO]
        for detalle in self.__pedido.obtener_detalles():
            descripcion = detalle.obtener_producto().obtener_nombre()
            cantidad = str(detalle.obtener_cantidad()).rjust(4)
            importe = f"{detalle.calcular_subtotal():.2f}".rjust(12)
            lineas.append(cantidad + "  " + recortar(descripcion, 42).ljust(42) + importe)
        return lineas

    def _pie(self):
        fecha = self.__fecha_emision.strftime("%d/%m/%Y %H:%M:%S")
        return [
            "-" * ANCHO,
            "Medio de pago: " + self.__medio_pago,
            "Fecha: " + fecha,
            "=" * ANCHO,
        ]

    @abstractmethod
    def obtener_tipo(self):
        pass

    @abstractmethod
    def imprimir(self):
        pass

    def __str__(self):
        return (f"{self.obtener_numero_completo()} - {self.obtener_tipo()}"
                f" - Pedido {self.__pedido.obtener_numero()} - {self.__medio_pago}"
                f" - Total S/ {self.calcular_total():.2f}")


class Boleta(Comprobante):

    def __init__(self, correlativo, pedido, medio_pago, dni_cliente="", nombre_cliente=""):
        super().__init__("B001", correlativo, pedido, medio_pago)
        if dni_cliente and (len(dni_cliente) != 8 or not dni_cliente.isdigit()):
            raise ValueError("El DNI debe tener ocho digitos numericos.")
        self.__dni_cliente = dni_cliente
        self.__nombre_cliente = nombre_cliente

    def obtener_tipo(self):
        return "Boleta"

    def imprimir(self):
        pedido = self.obtener_pedido()
        lineas = [
            "=" * ANCHO,
            ("BOLETA DE VENTA " + self.obtener_numero_completo()).center(ANCHO),
            "SAKURAMAKI S.A.C. - RUC 20601234567".center(ANCHO),
            "=" * ANCHO,
        ]
        if self.__nombre_cliente:
            lineas.extend([
                "Cliente: " + self.__nombre_cliente,
                "DNI: " + self.__dni_cliente,
                "-" * ANCHO,
            ])
        lineas.extend(self._lineas_detalle())
        precio_venta = f"S/ {pedido.calcular_subtotal():.2f}"
        recargo = f"S/ {pedido.calcular_recargo():.2f}"
        total = f"S/ {self.calcular_total():.2f}"
        lineas.extend([
            "-" * ANCHO,
            "Precio de venta".ljust(48) + precio_venta.rjust(16),
            "Recargo al consumo".ljust(48) + recargo.rjust(16),
            "TOTAL A PAGAR".ljust(48) + total.rjust(16),
        ])
        lineas.extend(self._pie())
        return "\n".join(lineas)

    def __str__(self):
        texto = super().__str__()
        if self.__nombre_cliente:
            texto = texto + f" - Cliente {self.__nombre_cliente} (DNI {self.__dni_cliente})"
        return texto


class Factura(Comprobante):

    def __init__(self, correlativo, pedido, medio_pago, ruc, razon_social):
        if len(ruc) != 11 or not ruc.isdigit():
            raise ValueError("El RUC debe tener once digitos numericos.")
        if not razon_social.strip():
            raise ValueError("La razon social no puede quedar vacia.")
        super().__init__("F001", correlativo, pedido, medio_pago)
        self.__ruc = ruc
        self.__razon_social = razon_social.strip()

    def validar_ruc(self):
        return len(self.__ruc) == 11 and self.__ruc.isdigit()

    def obtener_ruc(self):
        return self.__ruc

    def obtener_razon_social(self):
        return self.__razon_social

    def calcular_valor_venta(self):
        return self.obtener_pedido().calcular_subtotal() / (1 + IGV)

    def calcular_igv(self):
        return self.obtener_pedido().calcular_subtotal() - self.calcular_valor_venta()

    def obtener_tipo(self):
        return "Factura"

    def imprimir(self):
        pedido = self.obtener_pedido()
        lineas = [
            "=" * ANCHO,
            ("FACTURA " + self.obtener_numero_completo()).center(ANCHO),
            "SAKURAMAKI S.A.C. - RUC 20601234567".center(ANCHO),
            "=" * ANCHO,
            "Adquirente: " + self.__razon_social,
            "RUC: " + self.__ruc,
            "-" * ANCHO,
        ]
        lineas.extend(self._lineas_detalle())
        valor_venta = f"S/ {self.calcular_valor_venta():.2f}"
        igv = f"S/ {self.calcular_igv():.2f}"
        precio_venta = f"S/ {pedido.calcular_subtotal():.2f}"
        recargo = f"S/ {pedido.calcular_recargo():.2f}"
        total = f"S/ {self.calcular_total():.2f}"
        lineas.extend([
            "-" * ANCHO,
            "Valor de venta".ljust(48) + valor_venta.rjust(16),
            "IGV (18%)".ljust(48) + igv.rjust(16),
            "Precio de venta".ljust(48) + precio_venta.rjust(16),
            "Recargo al consumo".ljust(48) + recargo.rjust(16),
            "TOTAL A PAGAR".ljust(48) + total.rjust(16),
        ])
        lineas.extend(self._pie())
        return "\n".join(lineas)

    def __str__(self):
        return super().__str__() + f" - {self.__razon_social} (RUC {self.__ruc})"
