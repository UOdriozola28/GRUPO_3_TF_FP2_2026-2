from utiles import validaciones


def menu(restaurante):
    validaciones.titulo("GESTION DE PEDIDOS")
    print(" NUMERO         CANAL        ESTADO              TOTAL")
    print(" " + "-" * 58)
    for pedido in restaurante.listar_pedidos():
        print(" %-14s %-12s %-18s S/ %8.2f" % (
            pedido.obtener_numero(), pedido.obtener_canal(),
            pedido.obtener_estado(), pedido.calcular_total()))
    print("\n   Este modulo corresponde al integrante responsable de pedidos.")
    validaciones.pausar()
