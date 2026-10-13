from sistema.restaurante import Restaurante
from utiles import validaciones, datos_iniciales
from modulos import mantenimiento, pedidos, facturacion

def mostrar_portada():
    print("")
    print("+" + "-" * 68 + "+")
    print("|"+ "SAKURAMAKI S.A.C. - SISTEMA DE PEDIDOS Y FACTURACION" .center(68) + "|")
    print("|"+ "Version 1.0".center(68) + "|")
    print("+" + "-" * 68 + "+")

def main():
    restaurante = Restaurante("SakuraMaki S.A.C.", "20601234567")
    datos_iniciales.cargar_datos(restaurante)

    opcion = -1
    while opcion !=0:
        mostrar_portada()
        print("")
        print("     MENU PRINCIPAL")
        print("")
        print("     [1] Mantenimiento de datos maestros ")
        print("     [2] Gestion de pedidos")
        print("     [3] Facturacion")
        print("     [0] Salir del sistema")
        print("")
        opcion = validaciones.leer_entero("Seleccione una opcion [0-3]: ", 0 ,3)

        if opcion == 1:
            mantenimiento.menu(restaurante)
        elif opcion == 2:
            pedidos.menu(restaurante)
        elif opcion ==3:
            facturacion.menu(restaurante)

    print("")
    print(" Gracias por usar el sistema. Hasta pronto :3")
    print("")

if __name__ == "__main__":
    main()
