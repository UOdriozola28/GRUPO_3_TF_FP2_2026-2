"""Pantallas del modulo de facturacion (HU-10, HU-11 y HU-12)."""

from utiles import validaciones


def menu(restaurante):
    while True:
        validaciones.titulo("MODULO DE FACTURACION")
        print("   [1] Emitir comprobante y cerrar pedido")
        print("   [2] Ver comprobantes emitidos")
        print("   [0] Volver al menu principal\n")
        opcion = validaciones.leer_entero(" Seleccione una opcion [0-2]: ", 0, 2)
        if opcion == 0:
            return
        if opcion == 1:
            emitir_comprobante(restaurante)
        else:
            listar_comprobantes(restaurante)


def _buscar_pedido(restaurante):
    print("   Buscar pedido por: [1] Numero  [2] Mesa")
    forma = validaciones.leer_entero("   Opcion ................: ", 1, 2)
    if forma == 1:
        numero = validaciones.leer_texto("   Numero de pedido ......: ").upper()
        return restaurante.buscar_pedido_por_numero(numero)
    numero_mesa = validaciones.leer_entero("   Numero de mesa ........: ", 1, 18)
    return restaurante.buscar_pedido_por_mesa(numero_mesa)


def _mostrar_resumen(pedido):
    print("\n   Pedido: %-14s Estado: %s" % (pedido.obtener_numero(), pedido.obtener_estado()))
    print("   " + "-" * 60)
    for detalle in pedido.obtener_detalles():
        nombre = detalle.obtener_producto().obtener_nombre()
        print("   %3d  %-38s S/ %8.2f" %
              (detalle.obtener_cantidad(), nombre[:38], detalle.calcular_subtotal()))
    print("   " + "-" * 60)
    print("   Valor de venta .................. S/ %8.2f" %
          (pedido.calcular_subtotal() / 1.18))
    print("   IGV (18%%) ........................ S/ %8.2f" %
          (pedido.calcular_subtotal() - pedido.calcular_subtotal() / 1.18))
    print("   Precio de venta ................. S/ %8.2f" % pedido.calcular_subtotal())
    print("   Recargo al consumo .............. S/ %8.2f" % pedido.calcular_recargo())
    print("   TOTAL A PAGAR ................... S/ %8.2f" % pedido.calcular_total())


def emitir_comprobante(restaurante):
    validaciones.titulo("FACTURACION > EMITIR COMPROBANTE")
    pedido = _buscar_pedido(restaurante)
    if pedido is None:
        print("\n  [!] ERROR: no se encontro el pedido.")
        validaciones.pausar()
        return
    if not pedido.esta_listo():
        print("\n  [!] ERROR: el pedido debe encontrarse en estado Listo.")
        validaciones.pausar()
        return
    if not pedido.obtener_detalles():
        print("\n  [!] ERROR: el pedido no tiene productos registrados.")
        validaciones.pausar()
        return

    print("\n   Estado del pedido ......: " + pedido.obtener_estado())
    codigo_cajero = validaciones.leer_texto("   Codigo del cajero ......: ").upper()
    try:
        cajero = restaurante.buscar_cajero_activo(codigo_cajero)
    except ValueError as error:
        print("\n  [!] ERROR: " + str(error))
        validaciones.pausar()
        return
    print("   Cajero .................: " + cajero.obtener_nombres())

    print("\n   Tipo de comprobante: [1] Boleta  [2] Factura")
    tipo = validaciones.leer_entero("   Opcion ................: ", 1, 2)
    datos_cliente = ()
    if tipo == 1:
        if validaciones.confirmar("   Registrar datos del cliente? [S/N]: "):
            datos_cliente = (
                validaciones.leer_dni("   DNI del cliente .......: "),
                validaciones.leer_texto("   Nombre del cliente ....: "),
            )
        else:
            datos_cliente = ("", "")
    else:
        datos_cliente = (
            validaciones.leer_ruc("   RUC del adquirente ....: "),
            validaciones.leer_texto("   Razon social ..........: "),
        )

    print("\n   Medio de pago: [1] Efectivo  [2] Tarjeta  [3] Billetera digital")
    opcion_pago = validaciones.leer_entero("   Opcion ................: ", 1, 3)
    medio_pago = ("Efectivo", "Tarjeta", "Billetera digital")[opcion_pago - 1]
    _mostrar_resumen(pedido)

    if not validaciones.confirmar("\n   Confirmar la emision y el cobro? [S/N]: "):
        print("\n  [i] Operacion cancelada. El pedido permanece en estado Listo.")
        validaciones.pausar()
        return

    try:
        if tipo == 1:
            comprobante = restaurante.emitir_boleta(
                pedido, medio_pago, cajero, datos_cliente[0], datos_cliente[1]
            )
        else:
            comprobante = restaurante.emitir_factura(
                pedido, medio_pago, cajero, datos_cliente[0], datos_cliente[1]
            )
    except ValueError as error:
        print("\n  [!] ERROR: " + str(error))
        validaciones.pausar()
        return

    print("\n" + comprobante.imprimir())
    print("\n  [OK] Pedido pagado y comprobante emitido correctamente.")
    if pedido.obtener_mesa() is not None:
        print("  [OK] Mesa %02d liberada." % pedido.obtener_mesa().obtener_numero())
    validaciones.pausar()


def listar_comprobantes(restaurante):
    validaciones.titulo("FACTURACION > COMPROBANTES EMITIDOS")
    comprobantes = restaurante.listar_comprobantes()
    if not comprobantes:
        print("   Todavia no se ha emitido ningun comprobante.")
        validaciones.pausar()
        return

    print(" NUMERO         TIPO       PEDIDO        MEDIO DE PAGO       TOTAL S/")
    print(" " + "-" * 68)
    for comprobante in comprobantes:
        print(" %-14s %-10s %-13s %-20s %9.2f" % (
            comprobante.obtener_numero_completo(),
            comprobante.obtener_tipo(),
            comprobante.obtener_pedido().obtener_numero(),
            comprobante.obtener_medio_pago(),
            comprobante.calcular_total(),
        ))
    print(" " + "-" * 68)
    print(" Venta acumulada: S/ %.2f" % sum(c.calcular_total() for c in comprobantes))
    validaciones.pausar()
