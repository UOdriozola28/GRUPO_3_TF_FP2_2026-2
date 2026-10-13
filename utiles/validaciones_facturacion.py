"""Validaciones sencillas para las entradas de consola."""


def leer_entero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje))
            if numero < minimo or numero > maximo:
                raise ValueError
            return numero
        except ValueError:
            print("  [!] ERROR: ingrese un numero entre %d y %d." % (minimo, maximo))


def leer_texto(mensaje):
    while True:
        try:
            texto = input(mensaje).strip()
            if texto == "":
                raise ValueError
            return texto
        except ValueError:
            print("  [!] ERROR: el dato no puede quedar vacio.")


def leer_dni(mensaje):
    while True:
        try:
            dni = input(mensaje).strip()
            if len(dni) != 8 or not dni.isdigit():
                raise ValueError
            return dni
        except ValueError:
            print("  [!] ERROR: el DNI debe tener 8 digitos numericos.")


def leer_ruc(mensaje):
    while True:
        try:
            ruc = input(mensaje).strip()
            if len(ruc) != 11 or not ruc.isdigit():
                raise ValueError
            return ruc
        except ValueError:
            print("  [!] ERROR: el RUC debe tener 11 digitos numericos.")


def confirmar(mensaje):
    while True:
        try:
            respuesta = input(mensaje).strip().upper()
            if respuesta not in ("S", "N"):
                raise ValueError
            return respuesta == "S"
        except ValueError:
            print("  [!] ERROR: responda con S o N.")


def titulo(texto):
    print("\n+" + "-" * 68 + "+")
    print("| " + texto.ljust(66) + " |")
    print("+" + "-" * 68 + "+")


def pausar():
    input("\n Presione ENTER para continuar...")
