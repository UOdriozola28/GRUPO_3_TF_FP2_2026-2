"""Interfaz de consola del modulo de facturacion."""

from modelo.comprobante import IGV
from utiles import validaciones_facturacion as validaciones


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


def _buscar_cajero(restaurante):
    codigo = validaciones.leer_texto("   Codigo del cajero ......: ").upper()
    cajero = restaurante.buscar_empleado(codigo)
    if cajero is None:
        raise ValueError("El empleado %s no se encuentra registrado." % codigo)
    if hasattr(cajero, "esta_activo") and not cajero.esta_activo():
        raise ValueError("El empleado %s no se encuentra activo." % codigo)
    if cajero.obtener_tipo() != "Cajero":
        raise ValueError("El empleado %s no tiene el rol Cajero." % codigo)
    return cajero


def _mostrar_resumen(pedido):
    subtotal = pedido.calcular_subtotal()
    valor_venta = subtotal / (1 + IGV)
    print("\n   Pedido: %-14s Estado: %s" % (pedido.obtener_numero(), pedido.obtener_estado()))
    print("   " + "-" * 60)
    for detalle in pedido.obtener_detalles():
        print("   %3d  %-38s S/ %8.2f" % (
            detalle.obtener_cantidad(),
            detalle.obtener_producto().obtener_nombre()[:38],
            detalle.calcular_subtotal(),
        ))
    print("   " + "-" * 60)
    print("   Valor de venta .................. S/ %8.2f" % valor_venta)
    print("   IGV (18%%) ........................ S/ %8.2f" % (subtotal - valor_venta))
    print("   Precio de venta ................. S/ %8.2f" % subtotal)
    print("   Recargo al consumo .............. S/ %8.2f" % pedido.calcular_recargo())
    print("   TOTAL A PAGAR ................... S/ %8.2f" % pedido.calcular_total())


def _validar_pedido(pedido):
    """Comprueba las condiciones necesarias antes de facturar."""
    if pedido is None:
        raise ValueError("No se encontro el pedido.")
    if pedido.obtener_estado() != "Listo":
        raise ValueError("El pedido debe encontrarse en estado Listo.")
    if len(pedido.obtener_detalles()) == 0:
        raise ValueError("El pedido no tiene productos registrados.")


def _solicitar_datos_cliente(tipo):
    """Retorna el documento y el nombre segun el tipo de comprobante."""
    if tipo == 1:
        if validaciones.confirmar("   Registrar datos del cliente? [S/N]: "):
            dni = validaciones.leer_dni("   DNI del cliente .......: ")
            nombre = validaciones.leer_texto("   Nombre del cliente ....: ")
            return dni, nombre
        return "", ""

    ruc = validaciones.leer_ruc("   RUC del adquirente ....: ")
    razon_social = validaciones.leer_texto("   Razon social ..........: ")
    return ruc, razon_social


def _seleccionar_medio_pago():
    print("\n   Medio de pago: [1] Efectivo  [2] Tarjeta  [3] Billetera digital")
    opcion = validaciones.leer_entero("   Opcion ................: ", 1, 3)
    medios = ("Efectivo", "Tarjeta", "Billetera digital")
    return medios[opcion - 1]


def _generar_comprobante(restaurante, tipo, pedido, medio_pago, documento, cliente):
    """Delega la creacion al objeto restaurante."""
    if tipo == 1:
        return restaurante.emitir_boleta(pedido, medio_pago, documento, cliente)
    return restaurante.emitir_factura(pedido, medio_pago, documento, cliente)


def emitir_comprobante(restaurante):
    validaciones.titulo("FACTURACION > EMITIR COMPROBANTE")
    pedido = _buscar_pedido(restaurante)
    try:
        _validar_pedido(pedido)
    except ValueError as error:
        print("\n  [!] ERROR: " + str(error))
        validaciones.pausar()
        return

    print("\n   Estado del pedido ......: " + pedido.obtener_estado())
    try:
        cajero = _buscar_cajero(restaurante)
    except ValueError as error:
        print("\n  [!] ERROR: " + str(error))
        validaciones.pausar()
        return
    print("   Cajero .................: " + cajero.obtener_nombres())

    print("\n   Tipo de comprobante: [1] Boleta  [2] Factura")
    tipo = validaciones.leer_entero("   Opcion ................: ", 1, 2)
    documento, cliente = _solicitar_datos_cliente(tipo)
    medio_pago = _seleccionar_medio_pago()
    _mostrar_resumen(pedido)

    if not validaciones.confirmar("\n   Confirmar la emision y el cobro? [S/N]: "):
        print("\n  [i] Operacion cancelada. El pedido permanece en estado Listo.")
        validaciones.pausar()
        return

    try:
        comprobante = _generar_comprobante(
            restaurante, tipo, pedido, medio_pago, documento, cliente
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
    if len(comprobantes) == 0:
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
