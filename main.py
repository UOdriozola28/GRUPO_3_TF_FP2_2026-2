from modulos import facturacion, mantenimiento, pedidos
from sistema.restaurante import Restaurante
from utiles import datos_iniciales, validaciones


def main():
    restaurante = Restaurante("SakuraMaki S.A.C.", "20601234567")
    datos_iniciales.cargar_datos(restaurante)
    while True:
        validaciones.titulo("SAKURAMAKI - SISTEMA DE PEDIDOS Y FACTURACION")
        print("   [1] Mantenimiento de datos maestros")
        print("   [2] Gestion de pedidos")
        print("   [3] Facturacion")
        print("   [0] Salir del sistema\n")
        opcion = validaciones.leer_entero(" Seleccione una opcion [0-3]: ", 0, 3)
        if opcion == 0:
            print("\n Hasta pronto.\n")
            return
        (mantenimiento.menu, pedidos.menu, facturacion.menu)[opcion - 1](restaurante)


if __name__ == "__main__":
    main()
