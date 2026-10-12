def leer_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print("  [!] ERROR: debe estar entre %d y %d." % (minimo, maximo))
        except ValueError:
            print("  [!] ERROR: debe ingresar un numero entero.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  [!] ERROR: este dato no puede quedar vacio.")


def leer_dni(mensaje):
    while True:
        texto = input(mensaje).strip()
        if len(texto) == 8 and texto.isdigit():
            return texto
        print("  [!] ERROR: el DNI debe tener ocho digitos numericos.")


def leer_ruc(mensaje):
    while True:
        texto = input(mensaje).strip()
        if len(texto) == 11 and texto.isdigit():
            return texto
        print("  [!] ERROR: el RUC debe tener once digitos numericos.")


def confirmar(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        print("  [!] ERROR: responda con S o N.")


def pausar():
    input("\n Presione ENTER para continuar...")


def titulo(texto):
    print("\n+" + "-" * 68 + "+")
    print("| " + texto.ljust(66) + " |")
    print("+" + "-" * 68 + "+")
