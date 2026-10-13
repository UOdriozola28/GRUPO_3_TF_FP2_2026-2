from utiles import validaciones

def menu(restaurante):
    opcion = -1
    while opcion != 0:
        validaciones.titulo("GESTION DE PEDIDOS")
        print("   [1] Registrar nuevo pedido")
        print("   [2] Agregar productos a un pedido")
        print("   [3] Buscar pedido")
        print("   [0] Volver al menu principal")
        print("")
        opcion = validaciones.leer_entero(" Seleccione una opcion [0-3]: ", 0, 3)

        if opcion == 1:
            registrar_pedido(restaurante)
        elif opcion == 2:
            agregar_productos(restaurante)
        elif opcion == 3:
            buscar_pedido(restaurante)


# ---------------------------------------------------------------- HU-05
def registrar_pedido(restaurante):
    validaciones.titulo("PEDIDOS > NUEVO PEDIDO")

    print("   Canal de atencion  [1] Salon  [2] Para llevar  [3] Delivery")
    opcion_canal = validaciones.leer_entero("   Opcion .................: ", 1, 3)

    mesa = None
    if opcion_canal == 1:
        canal = "Salon"
        libres = restaurante.listar_mesas_libres()
        if len(libres) == 0:
            print("  [!] No hay mesas libres en este momento.")
            validaciones.pausar()
            return
        texto_mesas = ""
        for m in libres:
            texto_mesas = texto_mesas + str(m.obtener_numero()).rjust(2) + "  "
        print("")
        print("   Mesas disponibles: " + texto_mesas)
        numero_mesa = validaciones.leer_entero("   Numero de mesa .........: ", 1, 18)
        mesa = restaurante.buscar_mesa(numero_mesa)
        if mesa is None:
            print("  [!] ERROR: la mesa " + str(numero_mesa) + " no existe.")
            validaciones.pausar()
            return
        if not mesa.esta_libre():
            print("  [!] ERROR: la mesa " + str(numero_mesa) + " esta ocupada.")
            validaciones.pausar()
            return
    elif opcion_canal == 2:
        canal = "Para llevar"
    else:
        canal = "Delivery"

    mozos = restaurante.listar_mozos()
    if len(mozos) == 0:
        print("  [!] No hay mozos registrados. Registre uno antes de continuar.")
        validaciones.pausar()
        return

    print("")
    print("   Mozos disponibles:")
    for mozo in mozos:
        print("      " + mozo.obtener_codigo() + "  ->  " + mozo.obtener_nombres())

    mozo_elegido = None
    while mozo_elegido is None:
        codigo = validaciones.leer_texto("   Codigo del mozo ........: ").upper()
        empleado = restaurante.buscar_empleado(codigo)
        if empleado is None:
            print("  [!] ERROR: el codigo " + codigo + " no existe.")
        elif empleado.obtener_tipo() != "Mozo":
            print("  [!] ERROR: el empleado " + codigo + " no es un mozo.")
        else:
            mozo_elegido = empleado

    pedido = restaurante.registrar_pedido(canal, mesa, mozo_elegido)

    print("")
    print("   Pedido generado: " + pedido.obtener_numero())
    print("   Fecha y hora: " + pedido.obtener_fecha_hora().strftime("%d/%m/%Y %H:%M"))
    print("   Estado: " + pedido.obtener_estado().upper())
    print("")

    if validaciones.confirmar(" Desea agregar productos ahora? [S/N]: "):
        cargar_items(restaurante, pedido)
    else:
        validaciones.pausar()


# ---------------------------------------------------------------- HU-06
def agregar_productos(restaurante):
    validaciones.titulo("PEDIDOS > AGREGAR PRODUCTOS")
    numero = validaciones.leer_texto("   Numero de pedido .......: ").upper()
    pedido = restaurante.buscar_pedido_por_numero(numero)

    if pedido is None:
        print("  [!] ERROR: no existe el pedido " + numero + ".")
        validaciones.pausar()
        return

    if pedido.esta_pagado():
        print("  [!] ERROR: el pedido " + numero + " ya fue pagado y no se puede modificar.")
        validaciones.pausar()
        return

    cargar_items(restaurante, pedido)


def cargar_items(restaurante, pedido):
    """Bucle de carga de productos sobre un pedido abierto."""
    seguir = True
    while seguir:
        mostrar_pedido(pedido)
        print("")
        print("   [1] Agregar producto    [2] Quitar una linea")
        print("   [3] Enviar a cocina     [0] Volver")
        opcion = validaciones.leer_entero(" Seleccione una opcion [0-3]: ", 0, 3)

        if opcion == 1:
            codigo = validaciones.leer_texto("   Codigo del producto ....: ").upper()
            producto = restaurante.buscar_producto(codigo)
            if producto is None:
                print("  [!] ERROR: el codigo " + codigo + " no existe en la carta.")
                print("      Verifique el codigo o consulte el listado de productos.")
            else:
                cantidad = validaciones.leer_cantidad("   Cantidad ...............: ")
                try:
                    pedido.agregar_detalle(producto, cantidad)
                    print("  [OK] Agregado: " + producto.obtener_nombre())
                except ValueError as error:
                    print("  [!] ERROR: " + str(error))

        elif opcion == 2:
            if len(pedido.obtener_detalles()) == 0:
                print("  [!] El pedido no tiene lineas que quitar.")
            else:
                linea = validaciones.leer_entero("   Numero de linea a quitar: ", 1, len(pedido.obtener_detalles()))
                try:
                    pedido.quitar_detalle(linea - 1)
                    print("  [OK] Linea eliminada.")
                except IndexError as error:
                    print("  [!] ERROR: " + str(error))
                except ValueError as error:
                    print("  [!] ERROR: " + str(error))

        elif opcion == 3:
            if len(pedido.obtener_detalles()) == 0:
                print("  [!] No se puede enviar a cocina un pedido vacio.")
            else:
                pedido.cambiar_estado("En preparacion")
                print("  [OK] El pedido paso al estado EN PREPARACION.")
                seguir = False

        else:
            seguir = False

    validaciones.pausar()


def mostrar_pedido(pedido):
    """Muestra las lineas del pedido y el acumulado."""
    print("")
    if pedido.obtener_mesa() is None:
        ubicacion = pedido.obtener_canal()
    else:
        ubicacion = "Mesa " + str(pedido.obtener_mesa().obtener_numero())
    print(" PEDIDO " + pedido.obtener_numero() + "   " + ubicacion + "   Estado: " + pedido.obtener_estado())
    print(" " + "-" * 66)
    print(" N  COD      DESCRIPCION                 CANT   P.UNIT   SUBTOTAL")
    print(" " + "-" * 66)

    detalles = pedido.obtener_detalles()
    if len(detalles) == 0:
        print("    (el pedido todavia no tiene productos)")
    else:
        numero_linea = 1
        for detalle in detalles:
            producto = detalle.obtener_producto()
            texto = str(numero_linea).rjust(2) + "  "
            texto = texto + producto.obtener_codigo().ljust(9)
            texto = texto + producto.obtener_nombre().ljust(28)
            texto = texto + str(detalle.obtener_cantidad()).rjust(4)
            texto = texto + ("%.2f" % detalle.obtener_precio_unitario()).rjust(9)
            texto = texto + ("%.2f" % detalle.calcular_subtotal()).rjust(11)
            print(" " + texto)
            numero_linea = numero_linea + 1

    print(" " + "-" * 66)
    print(" Subtotal ................................. S/ %.2f" % pedido.calcular_subtotal())
    if pedido.calcular_recargo() > 0:
        print(" Recargo al consumo (10%%) ................. S/ %.2f" % pedido.calcular_recargo())
    print(" TOTAL .................................... S/ %.2f" % pedido.calcular_total())


# ---------------------------------------------------------------- HU-08
def buscar_pedido(restaurante):
    validaciones.titulo("PEDIDOS > BUSCAR PEDIDO")
    print("   Buscar por  [1] Numero de pedido   [2] Mesa")
    opcion = validaciones.leer_entero("   Opcion .................: ", 1, 2)

    if opcion == 1:
        numero = validaciones.leer_texto("   Numero de pedido .......: ").upper()
        pedido = restaurante.buscar_pedido_por_numero(numero)
    else:
        numero_mesa = validaciones.leer_entero("   Numero de mesa .........: ", 1, 18)
        pedido = restaurante.buscar_pedido_por_mesa(numero_mesa)

    if pedido is None:
        print("")
        print("  [!] No se encontro ningun pedido con ese criterio.")
    else:
        mostrar_pedido(pedido)

    validaciones.pausar()
