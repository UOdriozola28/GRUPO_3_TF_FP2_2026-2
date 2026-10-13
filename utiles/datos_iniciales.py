from modelo.producto import Plato, Bebida, Combo
from modelo.empleado import Mozo, Cocinero, Repartidor
from modelo.mesa import Mesa


def cargar_datos(restaurante):
    cargar_productos(restaurante)
    cargar_empleados(restaurante)
    cargar_mesas(restaurante)


def cargar_productos(restaurante):
    maki = Plato("MAK01", "Maki acevichado", 22.00, "Personal")
    ramen = Plato("RAM01", "Ramen tonkotsu", 26.00, "Personal")
    gyoza = Plato("GYO01", "Gyoza de cerdo", 18.00, "Personal")
    donburi = Plato("DON01", "Donburi de pollo", 24.00, "Personal")
    te = Bebida("BEB03", "Te verde frio 1 L", 12.00, "1 litro")
    gaseosa = Bebida("BEB05", "Gaseosa personal", 6.00, "500 ml")

    restaurante.registrar_producto(maki)
    restaurante.registrar_producto(ramen)
    restaurante.registrar_producto(gyoza)
    restaurante.registrar_producto(donburi)
    restaurante.registrar_producto(te)
    restaurante.registrar_producto(gaseosa)

    combo = Combo("CMB02", "Combo Duo Sakura", 0.15)
    combo.agregar_componente(maki)
    combo.agregar_componente(ramen)
    combo.agregar_componente(te)
    restaurante.registrar_producto(combo)

def cargar_empleados(restaurante):
    restaurante.registrar_empleado(Mozo("EMP015", "Ana Quispe Rojas", "70458213", 1130.00, 0.08))
    restaurante.registrar_empleado(Mozo("EMP018", "Luis Ramos Diaz", "71256984", 1130.00, 0.08))
    restaurante.registrar_empleado(Cocinero("EMP004", "Rosa Tanaka Li", "09876543", 1600.00, "Sushi"))
    restaurante.registrar_empleado(Repartidor("EMP011", "Jose Torres Vega", "72345678", 1130.00, 3.50))


def cargar_mesas(restaurante):
    numero = 1
    while numero <= 18:
        if numero <= 12:
            capacidad = 4
        else:
            capacidad = 6
        restaurante.registrar_mesa(Mesa(numero, capacidad))
        numero = numero + 1
