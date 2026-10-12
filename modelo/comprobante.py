"""Jerarquia de comprobantes para las HU-10 y HU-11."""

from abc import ABC, abstractmethod
from datetime import datetime

IGV = 0.18
ANCHO = 64


class Comprobante(ABC):
    def __init__(self, serie, correlativo, pedido, medio_pago, cajero):
        self.__serie = serie
        self.__correlativo = correlativo
        self.__pedido = pedido
        self.__medio_pago = medio_pago
        self.__cajero = cajero
        self.__fecha_emision = datetime.now()

    def obtener_numero_completo(self):
        return "%s-%06d" % (self.__serie, self.__correlativo)

    def obtener_pedido(self):
        return self.__pedido

    def obtener_medio_pago(self):
        return self.__medio_pago

    def obtener_cajero(self):
        return self.__cajero

    def obtener_fecha_emision(self):
        return self.__fecha_emision

    def calcular_total(self):
        return self.__pedido.calcular_total()

    def _lineas_detalle(self):
        lineas = ["CANT  DESCRIPCION".ljust(52) + "IMPORTE"]
        lineas.append("-" * ANCHO)
        for detalle in self.__pedido.obtener_detalles():
            producto = detalle.obtener_producto()
            descripcion = producto.obtener_nombre()
            if hasattr(producto, "obtener_tamanio"):
                descripcion += " (" + producto.obtener_tamanio() + ")"
            lineas.append(
                str(detalle.obtener_cantidad()).rjust(4)
                + "  "
                + descripcion[:42].ljust(42)
                + ("%.2f" % detalle.calcular_subtotal()).rjust(12)
            )
        return lineas

    def _pie(self):
        return [
            "-" * ANCHO,
            "Medio de pago: " + self.__medio_pago,
            "Cajero: " + self.__cajero.obtener_codigo() + " - " + self.__cajero.obtener_nombres(),
            "Fecha: " + self.__fecha_emision.strftime("%d/%m/%Y %H:%M:%S"),
            "=" * ANCHO,
        ]

    @abstractmethod
    def obtener_tipo(self):
        pass

    @abstractmethod
    def imprimir(self):
        pass


class Boleta(Comprobante):
    def __init__(self, correlativo, pedido, medio_pago, cajero, dni_cliente="", nombre_cliente=""):
        super().__init__("B001", correlativo, pedido, medio_pago, cajero)
        self.__dni_cliente = dni_cliente
        self.__nombre_cliente = nombre_cliente

    def obtener_tipo(self):
        return "Boleta"

    def imprimir(self):
        pedido = self.obtener_pedido()
        lineas = ["=" * ANCHO, ("BOLETA DE VENTA " + self.obtener_numero_completo()).center(ANCHO),
                  "SAKURAMAKI S.A.C. - RUC 20601234567".center(ANCHO), "=" * ANCHO]
        if self.__nombre_cliente:
            lineas.extend(["Cliente: " + self.__nombre_cliente, "DNI: " + self.__dni_cliente, "-" * ANCHO])
        lineas.extend(self._lineas_detalle())
        lineas.extend([
            "-" * ANCHO,
            "Subtotal".ljust(48) + ("S/ %.2f" % pedido.calcular_subtotal()).rjust(16),
            "Recargo al consumo".ljust(48) + ("S/ %.2f" % pedido.calcular_recargo()).rjust(16),
            "TOTAL A PAGAR".ljust(48) + ("S/ %.2f" % self.calcular_total()).rjust(16),
        ])
        lineas.extend(self._pie())
        return "\n".join(lineas)


class Factura(Comprobante):
    def __init__(self, correlativo, pedido, medio_pago, cajero, ruc, razon_social):
        if len(ruc) != 11 or not ruc.isdigit():
            raise ValueError("El RUC debe tener once digitos numericos.")
        if not razon_social.strip():
            raise ValueError("La razon social no puede quedar vacia.")
        super().__init__("F001", correlativo, pedido, medio_pago, cajero)
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
        lineas = ["=" * ANCHO, ("FACTURA " + self.obtener_numero_completo()).center(ANCHO),
                  "SAKURAMAKI S.A.C. - RUC 20601234567".center(ANCHO), "=" * ANCHO,
                  "Adquirente: " + self.__razon_social, "RUC: " + self.__ruc, "-" * ANCHO]
        lineas.extend(self._lineas_detalle())
        lineas.extend([
            "-" * ANCHO,
            "Valor de venta".ljust(48) + ("S/ %.2f" % self.calcular_valor_venta()).rjust(16),
            "IGV (18%)".ljust(48) + ("S/ %.2f" % self.calcular_igv()).rjust(16),
            "Precio de venta".ljust(48) + ("S/ %.2f" % pedido.calcular_subtotal()).rjust(16),
            "Recargo al consumo".ljust(48) + ("S/ %.2f" % pedido.calcular_recargo()).rjust(16),
            "TOTAL A PAGAR".ljust(48) + ("S/ %.2f" % self.calcular_total()).rjust(16),
        ])
        lineas.extend(self._pie())
        return "\n".join(lineas)
