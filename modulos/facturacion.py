from modelo.comprobante import IGV
from utiles import validaciones
from utiles.formato import recortar


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
    subtotal = pedido.calcular_subtotal()
    valor_venta = subtotal / (1 + IGV)
    numero_pedido = pedido.obtener_numero().ljust(14)
    print(f"\n   Pedido: {numero_pedido} Estado: {pedido.obtener_estado()}")
    print("   " + "-" * 60)
    for detalle in pedido.obtener_detalles():
        cantidad = str(detalle.obtener_cantidad()).rjust(3)
        nombre = recortar(detalle.obtener_producto().obtener_nombre(), 38).ljust(38)
        importe = f"{detalle.calcular_subtotal():.2f}".rjust(8)
        print(f"   {cantidad}  {nombre} S/ {importe}")
    print("   " + "-" * 60)
    igv = subtotal - valor_venta
    print("   Valor de venta .................. S/ " + f"{valor_venta:.2f}".rjust(8))
    print("   IGV (18%) ........................ S/ " + f"{igv:.2f}".rjust(8))
    print("   Precio de venta ................. S/ " + f"{subtotal:.2f}".rjust(8))
    print("   Recargo al consumo .............. S/ " + f"{pedido.calcular_recargo():.2f}".rjust(8))
    print("   TOTAL A PAGAR ................... S/ " + f"{pedido.calcular_total():.2f}".rjust(8))


def _validar_pedido(pedido):
    if pedido is None:
        raise ValueError("No se encontro el pedido.")
    if pedido.esta_pagado():
        raise ValueError("El pedido ya fue pagado.")
    if len(pedido.obtener_detalles()) == 0:
        raise ValueError("El pedido no tiene productos registrados.")


def _solicitar_datos_cliente(tipo):
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

    print("\n   Tipo de comprobante: [1] Boleta  [2] Factura")
    tipo = validaciones.leer_entero("   Opcion ................: ", 1, 2)
    documento, cliente = _solicitar_datos_cliente(tipo)
    medio_pago = _seleccionar_medio_pago()
    _mostrar_resumen(pedido)

    if not validaciones.confirmar("\n   Confirmar la emision y el cobro? [S/N]: "):
        print("\n  [i] Operacion cancelada. El pedido no fue cobrado.")
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
        numero_mesa = str(pedido.obtener_mesa().obtener_numero()).rjust(2, "0")
        print(f"  [OK] Mesa {numero_mesa} liberada.")
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
    venta_acumulada = 0.0
    for comprobante in comprobantes:
        numero = comprobante.obtener_numero_completo().ljust(14)
        tipo = comprobante.obtener_tipo().ljust(10)
        pedido = comprobante.obtener_pedido().obtener_numero().ljust(13)
        medio_pago = comprobante.obtener_medio_pago().ljust(20)
        total = f"{comprobante.calcular_total():.2f}".rjust(9)
        print(f" {numero} {tipo} {pedido} {medio_pago} {total}")
        venta_acumulada = venta_acumulada + comprobante.calcular_total()
    print(" " + "-" * 68)
    print(f" Venta acumulada: S/ {venta_acumulada:.2f}")
    validaciones.pausar()
