from modelo.empleado import Cajero, Cocinero, Mozo, Repartidor
from modelo.mesa import Mesa
from modelo.producto import Bebida, Plato


def cargar_datos(restaurante):
    maki = Plato("MAK01", "Maki acevichado", 22.0, "Grande")
    gyoza = Plato("GYO01", "Gyoza de cerdo", 18.0)
    ramen = Plato("RAM01", "Ramen tonkotsu", 26.0)
    te = Bebida("BEB03", "Te verde frio 1 L", 12.0, "1 litro")
    for producto in (maki, gyoza, ramen, te):
        restaurante.registrar_producto(producto)

    restaurante.registrar_empleado(Mozo("EMP015", "Ana Quispe Rojas", "70458213", 1130, 0.08))
    restaurante.registrar_empleado(Cocinero("EMP004", "Rosa Tanaka Li", "09876543", 1600, "Sushi"))
    restaurante.registrar_empleado(Repartidor("EMP011", "Jose Torres Vega", "72345678", 1130, 3.50))
    restaurante.registrar_empleado(Cajero("EMP021", "Carlos Mendoza", "74632158", 1300))

    for numero in range(1, 19):
        restaurante.registrar_mesa(Mesa(numero, 4 if numero <= 12 else 6))

    # Pedido listo de demostracion para probar facturacion inmediatamente.
    mesa = restaurante.buscar_mesa(7)
    mozo = restaurante.buscar_empleado("EMP015")
    pedido = restaurante.registrar_pedido("Salon", mesa, mozo)
    pedido.agregar_detalle(maki, 2, mozo)
    pedido.agregar_detalle(gyoza, 1, mozo)
    pedido.agregar_detalle(ramen, 1, mozo)
    pedido.agregar_detalle(te, 1, mozo)
    pedido.cambiar_estado("En preparacion")
    pedido.cambiar_estado("Listo")
