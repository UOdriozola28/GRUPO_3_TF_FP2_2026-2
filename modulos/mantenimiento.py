from utiles import validaciones


def menu(restaurante):
    validaciones.titulo("MANTENIMIENTO DE DATOS")
    print("   Productos registrados: %d" % len(restaurante.listar_productos()))
    print("   Empleados registrados: %d" % len(restaurante.listar_empleados()))
    print("\n   Este modulo corresponde al integrante responsable de mantenimiento.")
    validaciones.pausar()
