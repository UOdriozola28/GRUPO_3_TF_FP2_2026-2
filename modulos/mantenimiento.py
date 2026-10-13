from modelo.producto import Plato, Bebida, Combo
from modelo.empleado import Mozo, Cocinero, Repartidor
from utiles import validaciones


def menu(restaurante):
    opcion = -1
    while opcion != 0:
        validaciones.titulo("MANTENIMIENTO DE DATOS MAESTROS")
        print("   [1] Registrar producto")
        print("   [2] Listar productos de la carta")
        print("   [3] Registrar empleado")
        print("   [4] Consultar remuneracion del personal")
        print("   [0] Volver al menu principal")
        print("")
        opcion = validaciones.leer_entero(" Seleccione una opcion [0-4]: ", 0, 4)

        if opcion == 1:
            registrar_producto(restaurante)
        elif opcion == 2:
            listar_productos(restaurante)
        elif opcion == 3:
            registrar_empleado(restaurante)
        elif opcion == 4:
            consultar_remuneraciones(restaurante)


# ---------------------------------------------------------------- HU-01
def registrar_producto(restaurante):
    validaciones.titulo("MANTENIMIENTO > REGISTRAR PRODUCTO")

    codigo = validaciones.leer_texto("   Codigo del producto ....: ").upper()
    if restaurante.buscar_producto(codigo) is not None:
        print("  [!] ERROR: el codigo " + codigo + " ya esta registrado.")
        validaciones.pausar()
        return

    nombre = validaciones.leer_texto("   Nombre .................: ")
    print("   Categoria [1] Plato  [2] Bebida  [3] Combo")
    categoria = validaciones.leer_entero("   Opcion .................: ", 1, 3)

    producto = None

    if categoria == 1:
        precio = validaciones.leer_decimal("   Precio base (S/) .......: ")
        print("   Tamano [1] Personal  [2] Mediano  [3] Grande")
        opcion_tamano = validaciones.leer_entero("   Opcion .................: ", 1, 3)
        if opcion_tamano == 1:
            tamano = "Personal"
        elif opcion_tamano == 2:
            tamano = "Mediano"
        else:
            tamano = "Grande"
        producto = Plato(codigo, nombre, precio, tamano)

    elif categoria == 2:
        precio = validaciones.leer_decimal("   Precio (S/) ............: ")
        presentacion = validaciones.leer_texto("   Presentacion ...........: ")
        producto = Bebida(codigo, nombre, precio, presentacion)

    else:
        descuento = validaciones.leer_decimal("   Descuento (ejemplo 0.15): ")
        producto = Combo(codigo, nombre, descuento)
        print("")
        print("   Agregue los productos que forman el combo.")
        seguir = True
        while seguir:
            codigo_componente = validaciones.leer_texto("   Codigo del componente ..: ").upper()
            componente = restaurante.buscar_producto(codigo_componente)
            if componente is None:
                print("  [!] ERROR: el codigo " + codigo_componente + " no existe en la carta.")
            else:
                producto.agregar_componente(componente)
                print("      Agregado: " + componente.obtener_nombre())
            seguir = validaciones.confirmar("   Agregar otro componente? [S/N]: ")
        if len(producto.obtener_componentes()) == 0:
            print("  [!] ERROR: un combo debe tener al menos un componente.")
            validaciones.pausar()
            return

    print("")
    print("   Precio calculado: S/ %.2f" % producto.calcular_precio())
    print("")

    if validaciones.confirmar(" Confirmar el registro? [S/N]: "):
        try:
            restaurante.registrar_producto(producto)
            print("  [OK] Producto registrado correctamente.")
        except ValueError as error:
            print("  [!] ERROR: " + str(error))
    else:
        print("  Registro cancelado.")

    validaciones.pausar()


# ---------------------------------------------------------------- HU-02
def listar_productos(restaurante):
    validaciones.titulo("MANTENIMIENTO > LISTADO DE PRODUCTOS")
    productos = restaurante.listar_productos()

    if len(productos) == 0:
        print("   No hay productos registrados.")
        validaciones.pausar()
        return

    print(" COD      DESCRIPCION                     CATEGORIA     PRECIO S/")
    print(" " + "-" * 66)
    for producto in productos:
        codigo = producto.obtener_codigo().ljust(9)
        nombre = producto.obtener_nombre().ljust(32)
        categoria = producto.obtener_categoria().ljust(14)
        precio = ("%.2f" % producto.calcular_precio()).rjust(9)
        print(" " + codigo + nombre + categoria + precio)
    print(" " + "-" * 66)
    print(" Productos registrados: " + str(len(productos)))
    validaciones.pausar()


# ---------------------------------------------------------------- HU-03
def registrar_empleado(restaurante):
    validaciones.titulo("MANTENIMIENTO > REGISTRAR EMPLEADO")

    codigo = validaciones.leer_texto("   Codigo .................: ").upper()
    if restaurante.buscar_empleado(codigo) is not None:
        print("  [!] ERROR: el codigo " + codigo + " ya esta registrado.")
        validaciones.pausar()
        return

    nombres = validaciones.leer_texto("   Nombres y apellidos ....: ")
    dni = validaciones.leer_dni("   DNI ....................: ")

    print("   Tipo de empleado:")
    print("       [1] Mozo        (basico + % de propina)")
    print("       [2] Cocinero    (remuneracion fija)")
    print("       [3] Repartidor  (basico + monto por entrega)")
    tipo = validaciones.leer_entero("   Opcion .................: ", 1, 3)

    basico = validaciones.leer_decimal("   Sueldo basico (S/) .....: ")

    if tipo == 1:
        porcentaje = validaciones.leer_decimal("   Porcentaje de propina (ej. 0.08): ")
        empleado = Mozo(codigo, nombres, dni, basico, porcentaje)
    elif tipo == 2:
        especialidad = validaciones.leer_texto("   Especialidad ...........: ")
        empleado = Cocinero(codigo, nombres, dni, basico)
    else:
        monto = validaciones.leer_decimal("   Monto por entrega (S/) .: ")
        empleado = Repartidor(codigo, nombres, dni, basico, monto)

    print("")
    if validaciones.confirmar(" Confirmar el registro? [S/N]: "):
        try:
            restaurante.registrar_empleado(empleado)
            print("  [OK] Empleado registrado correctamente.")
        except ValueError as error:
            print("  [!] ERROR: " + str(error))
    else:
        print("  Registro cancelado.")

    validaciones.pausar()


# ---------------------------------------------------------------- HU-04
def consultar_remuneraciones(restaurante):
    validaciones.titulo("MANTENIMIENTO > REMUNERACION DEL PERSONAL")
    empleados = restaurante.listar_empleados()

    if len(empleados) == 0:
        print("   No hay empleados registrados.")
        validaciones.pausar()
        return

    print(" CODIGO    EMPLEADO             TIPO          BASICO  VARIABLE     TOTAL")
    print(" " + "-" * 70)
    total_planilla = 0.0
    for empleado in empleados:
        codigo = empleado.obtener_codigo().ljust(10)
        nombre = empleado.obtener_nombres().ljust(21)
        tipo = empleado.obtener_tipo().ljust(12)
        basico = ("%.2f" % empleado.obtener_sueldo_basico()).rjust(8)
        remuneracion = empleado.calcular_remuneracion()
        variable = ("%.2f" % empleado.calcular_variable()).rjust(10)
        total = ("%.2f" % remuneracion).rjust(10)
        print(" " + codigo + nombre + tipo + basico + variable + total)
        total_planilla = total_planilla + remuneracion
    print(" " + "-" * 70)
    print(" Total de la planilla ..................... S/ %.2f" % total_planilla)
    validaciones.pausar()