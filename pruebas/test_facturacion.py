import unittest

from modelo.empleado import Cajero, Mozo
from modelo.mesa import Mesa
from modelo.producto import Plato
from sistema.restaurante import Restaurante


class PruebasFacturacion(unittest.TestCase):
    def setUp(self):
        self.restaurante = Restaurante("SakuraMaki S.A.C.", "20601234567")
        self.cajero = Cajero("EMP021", "Carlos Mendoza", "74632158", 1300)
        self.mozo = Mozo("EMP015", "Ana Quispe", "70458213", 1130, 0.08)
        self.mesa = Mesa(7, 4)
        self.producto = Plato("MAK01", "Maki acevichado", 22, "Grande")
        self.restaurante.registrar_empleado(self.cajero)
        self.restaurante.registrar_empleado(self.mozo)
        self.restaurante.registrar_mesa(self.mesa)
        self.restaurante.registrar_producto(self.producto)
        self.pedido = self.restaurante.registrar_pedido("Salon", self.mesa, self.mozo)
        self.pedido.agregar_detalle(self.producto, 4, self.mozo)

    def dejar_listo(self):
        self.pedido.cambiar_estado("En preparacion")
        self.pedido.cambiar_estado("Listo")

    def test_rechaza_pedido_que_no_esta_listo(self):
        with self.assertRaisesRegex(ValueError, "estado Listo"):
            self.restaurante.emitir_boleta(self.pedido, "Efectivo", self.cajero)

    def test_rechaza_empleado_que_no_es_cajero(self):
        self.dejar_listo()
        with self.assertRaisesRegex(ValueError, "rol Cajero"):
            self.restaurante.emitir_boleta(self.pedido, "Efectivo", self.mozo)

    def test_rechaza_ruc_invalido_sin_consumir_correlativo(self):
        self.dejar_listo()
        with self.assertRaisesRegex(ValueError, "once digitos"):
            self.restaurante.emitir_factura(self.pedido, "Tarjeta", self.cajero, "123", "Empresa")
        factura = self.restaurante.emitir_factura(
            self.pedido, "Tarjeta", self.cajero, "20512345678", "Inversiones Delta S.A.C."
        )
        self.assertEqual(factura.obtener_numero_completo(), "F001-000001")

    def test_factura_calcula_importes_del_diseno(self):
        self.dejar_listo()
        factura = self.restaurante.emitir_factura(
            self.pedido, "Tarjeta", self.cajero, "20512345678", "Inversiones Delta S.A.C."
        )
        self.assertAlmostEqual(factura.calcular_valor_venta(), 94.92, places=2)
        self.assertAlmostEqual(factura.calcular_igv(), 17.08, places=2)
        self.assertAlmostEqual(factura.calcular_total(), 123.20, places=2)

    def test_cierre_paga_pedido_y_libera_mesa(self):
        self.dejar_listo()
        self.restaurante.emitir_boleta(self.pedido, "Efectivo", self.cajero)
        self.assertTrue(self.pedido.esta_pagado())
        self.assertTrue(self.mesa.esta_libre())

    def test_comprobante_registra_cajero_y_medio_de_pago(self):
        self.dejar_listo()
        boleta = self.restaurante.emitir_boleta(self.pedido, "Billetera digital", self.cajero)
        self.assertIs(boleta.obtener_cajero(), self.cajero)
        self.assertEqual(boleta.obtener_medio_pago(), "Billetera digital")
        self.assertIn("TOTAL A PAGAR", boleta.imprimir())


if __name__ == "__main__":
    unittest.main(verbosity=2)
