"""Pantallas del modulo de facturacion - HU-10, HU-11 y HU-12."""

try:
    from utiles import validaciones
except (ModuleNotFoundError, ImportError):
    class ValidacionesConsola:
        """Validaciones minimas para ejecutar la preview sin otros modulos."""

        @staticmethod
        def titulo(texto):
            print("\n+" + "-" * 68 + "+")
            print("| " + texto.ljust(66) + " |")
            print("+" + "-" * 68 + "+")

        @staticmethod
        def leer_entero(mensaje, minimo, maximo):
            while True:
                try:
                    valor = int(input(mensaje))
                    if minimo <= valor <= maximo:
                        return valor
                except ValueError:
                    pass
                print("  [!] Ingrese un numero entre %d y %d." % (minimo, maximo))

        @staticmethod
        def leer_texto(mensaje):
            while True:
                texto = input(mensaje).strip()
                if texto:
                    return texto
                print("  [!] El dato no puede quedar vacio.")

        @staticmethod
        def leer_dni(mensaje):
            while True:
                dni = input(mensaje).strip()
                if len(dni) == 8 and dni.isdigit():
                    return dni
                print("  [!] El DNI debe tener 8 digitos.")

        @staticmethod
        def leer_ruc(mensaje):
            while True:
                ruc = input(mensaje).strip()
                if len(ruc) == 11 and ruc.isdigit():
                    return ruc
                print("  [!] El RUC debe tener 11 digitos.")

        @staticmethod
        def confirmar(mensaje):
            while True:
                respuesta = input(mensaje).strip().upper()
                if respuesta in ("S", "N"):
                    return respuesta == "S"
                print("  [!] Responda S o N.")

        @staticmethod
        def pausar():
            input("\n Presione ENTER para continuar...")

    validaciones = ValidacionesConsola()


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
    valor_venta = subtotal / 1.18
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


def emitir_comprobante(restaurante):
    validaciones.titulo("FACTURACION > EMITIR COMPROBANTE")
    pedido = _buscar_pedido(restaurante)
    if pedido is None:
        print("\n  [!] ERROR: no se encontro el pedido.")
        validaciones.pausar()
        return
    if pedido.obtener_estado() != "Listo":
        print("\n  [!] ERROR: el pedido debe encontrarse en estado Listo.")
        validaciones.pausar()
        return
    if len(pedido.obtener_detalles()) == 0:
        print("\n  [!] ERROR: el pedido no tiene productos registrados.")
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
    if tipo == 1:
        if validaciones.confirmar("   Registrar datos del cliente? [S/N]: "):
            documento = validaciones.leer_dni("   DNI del cliente .......: ")
            cliente = validaciones.leer_texto("   Nombre del cliente ....: ")
        else:
            documento, cliente = "", ""
    else:
        documento = validaciones.leer_ruc("   RUC del adquirente ....: ")
        cliente = validaciones.leer_texto("   Razon social ..........: ")

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
            comprobante = restaurante.emitir_boleta(pedido, medio_pago, documento, cliente)
        else:
            comprobante = restaurante.emitir_factura(pedido, medio_pago, documento, cliente)
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
