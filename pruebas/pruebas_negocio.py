import os
import sys

# Permite importar las carpetas del proyecto al ejecutar este archivo
carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, carpeta_proyecto)

from modelo.producto import Plato, Bebida, Combo
from modelo.empleado import Mozo, Cocinero, Repartidor
from modelo.mesa import Mesa
from modelo.pedido import Pedido
from modelo.comprobante import Factura
from sistema.restaurante import Restaurante

total_pruebas = 0
pruebas_ok = 0


def verificar(nombre, obtenido, esperado):
    global total_pruebas, pruebas_ok
    total_pruebas = total_pruebas + 1
    if obtenido == esperado:
        pruebas_ok = pruebas_ok + 1
        print(f"OK     {nombre}")
    else:
        print(f"FALLA  {nombre}: obtenido {obtenido}, esperado {esperado}")


def verificar_error(nombre, tipo_error, funcion, *argumentos):
    global total_pruebas, pruebas_ok
    total_pruebas = total_pruebas + 1
    try:
        funcion(*argumentos)
        print(f"FALLA  {nombre}: no se produjo ningun error")
    except tipo_error:
        pruebas_ok = pruebas_ok + 1
        print(f"OK     {nombre}")
    except Exception as error:
        print(f"FALLA  {nombre}: error distinto ({type(error).__name__})")


def crear_restaurante():
    restaurante = Restaurante("SakuraMaki S.A.C.", "20601234567")
    restaurante.registrar_empleado(Mozo("EMP001", "Ana Quispe", "70458213", 1130.00, 0.08))
    restaurante.registrar_mesa(Mesa(1, 4))
    return restaurante


# ---------------------------------------------------------------- Productos
print("--- Productos")
verificar("Plato personal", Plato("P1", "Maki", 22.0, "Personal").calcular_precio(), 22.0)
verificar("Plato mediano", Plato("P2", "Maki", 22.0, "Mediano").calcular_precio(), 25.0)
verificar("Plato grande", Plato("P3", "Maki", 22.0, "Grande").calcular_precio(), 28.0)
verificar("Bebida", Bebida("B1", "Te verde", 12.0, "1 litro").calcular_precio(), 12.0)

combo = Combo("C1", "Combo Duo", 0.15)
combo.agregar_componente(Plato("P1", "Maki", 22.0, "Personal"))
combo.agregar_componente(Plato("P4", "Ramen", 26.0, "Personal"))
combo.agregar_componente(Bebida("B1", "Te verde", 12.0, "1 litro"))
verificar("Combo con 15% de descuento", round(combo.calcular_precio(), 2), 51.0)

# ---------------------------------------------------------------- Empleados
print("--- Empleados")
mozo = Mozo("EMP001", "Ana Quispe", "70458213", 1130.00, 0.08)
mozo.registrar_propina(250.0)
verificar("Remuneracion del mozo", round(mozo.calcular_remuneracion(), 2), 1150.0)
verificar("Variable del mozo", round(mozo.calcular_variable(), 2), 20.0)

repartidor = Repartidor("EMP002", "Jose Torres", "72345678", 1130.00, 3.50)
repartidor.registrar_entrega()
repartidor.registrar_entrega()
repartidor.registrar_entrega()
repartidor.registrar_entrega()
verificar("Remuneracion del repartidor", round(repartidor.calcular_remuneracion(), 2), 1144.0)

cocinero = Cocinero("EMP003", "Rosa Tanaka", "09876543", 1600.00, "Sushi")
verificar("Remuneracion del cocinero", cocinero.calcular_remuneracion(), 1600.0)
verificar("Variable del cocinero", cocinero.calcular_variable(), 0.0)

# ---------------------------------------------------------------- Pedidos
print("--- Pedidos")
maki = Plato("MAK01", "Maki acevichado", 22.0, "Personal")
gaseosa = Bebida("BEB05", "Gaseosa personal", 6.0, "500 ml")

restaurante = crear_restaurante()
mesa = restaurante.buscar_mesa(1)
mozo = restaurante.buscar_empleado("EMP001")
pedido_salon = restaurante.registrar_pedido("Salon", mesa, mozo)
pedido_salon.agregar_detalle(maki, 2)
pedido_salon.agregar_detalle(gaseosa, 1)
verificar("Subtotal del pedido", pedido_salon.calcular_subtotal(), 50.0)
verificar("Recargo del salon (10%)", round(pedido_salon.calcular_recargo(), 2), 5.0)
verificar("Total del pedido en salon", round(pedido_salon.calcular_total(), 2), 55.0)
verificar("Cantidad de items", pedido_salon.contar_items(), 3)

pedido_delivery = restaurante.registrar_pedido("Delivery", None, mozo)
pedido_delivery.agregar_detalle(maki, 2)
verificar("El delivery no paga recargo", pedido_delivery.calcular_recargo(), 0.0)
verificar("Total del delivery", pedido_delivery.calcular_total(), 44.0)

# ---------------------------------------------------------------- Mesas
print("--- Mesas")
verificar("La mesa se ocupa al registrar el pedido", mesa.esta_libre(), False)
factura = restaurante.emitir_factura(pedido_salon, "Efectivo", "20123456789", "Empresa SAC")
verificar("La mesa se libera al pagar", mesa.esta_libre(), True)
verificar("El pedido queda pagado", pedido_salon.esta_pagado(), True)

# ---------------------------------------------------------------- Factura
print("--- Factura")
verificar("Valor de venta", round(factura.calcular_valor_venta(), 2), 42.37)
verificar("IGV", round(factura.calcular_igv(), 2), 7.63)
verificar("RUC valido", factura.validar_ruc(), True)
verificar("Numero de la factura", factura.obtener_numero_completo(), "F001-000001")

# ---------------------------------------------------------------- Errores
print("--- Errores")
restaurante.registrar_producto(maki)
verificar_error("Codigo de producto duplicado", ValueError, restaurante.registrar_producto, maki)
verificar_error("Codigo de empleado duplicado", ValueError, restaurante.registrar_empleado, mozo)

verificar_error("RUC invalido", ValueError, restaurante.emitir_factura, pedido_delivery, "Efectivo", "123", "Empresa SAC")
verificar_error("RUC con letras", ValueError, Factura, 2, pedido_delivery, "Efectivo", "2012345678A", "Empresa SAC")
verificar_error("Facturar un pedido ya pagado", ValueError, restaurante.emitir_boleta, pedido_salon, "Efectivo", "", "")
verificar_error("Facturar un pedido sin lineas", ValueError, restaurante.emitir_boleta, Pedido("PED-000098", "Delivery", None, mozo), "Efectivo", "", "")
verificar_error("Agregar a un pedido pagado", ValueError, pedido_salon.agregar_detalle, maki, 1)
verificar_error("Quitar de un pedido pagado", ValueError, pedido_salon.quitar_detalle, 0)

pedido_nuevo = Pedido("PED-000099", "Delivery", None, mozo)
pedido_nuevo.agregar_detalle(maki, 1)
verificar_error("Linea inexistente", IndexError, pedido_nuevo.quitar_detalle, 5)

print("")
print(f"Pruebas correctas: {pruebas_ok} de {total_pruebas}")
if pruebas_ok != total_pruebas:
    print(f"Pruebas con FALLA: {total_pruebas - pruebas_ok}")
