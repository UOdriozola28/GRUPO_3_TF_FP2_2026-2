from abc import ABC, abstractmethod


class Producto(ABC):
    def __init__(self, codigo, nombre):
        self.__codigo = codigo
        self.__nombre = nombre

    def obtener_codigo(self):
        return self.__codigo

    def obtener_nombre(self):
        return self.__nombre

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def obtener_tipo(self):
        pass


class Plato(Producto):
    INCREMENTOS = {"Personal": 0.0, "Mediano": 3.0, "Grande": 6.0}

    def __init__(self, codigo, nombre, precio_base, tamanio="Personal"):
        super().__init__(codigo, nombre)
        if tamanio not in self.INCREMENTOS:
            raise ValueError("El tamanio del plato no es valido.")
        self.__precio_base = float(precio_base)
        self.__tamanio = tamanio

    def calcular_precio(self):
        return self.__precio_base + self.INCREMENTOS[self.__tamanio]

    def obtener_tipo(self):
        return "Plato"

    def obtener_tamanio(self):
        return self.__tamanio


class Bebida(Producto):
    def __init__(self, codigo, nombre, precio, presentacion=""):
        super().__init__(codigo, nombre)
        self.__precio = float(precio)
        self.__presentacion = presentacion

    def calcular_precio(self):
        return self.__precio

    def obtener_tipo(self):
        return "Bebida"


class Combo(Producto):
    def __init__(self, codigo, nombre, porcentaje_descuento):
        super().__init__(codigo, nombre)
        self.__porcentaje_descuento = float(porcentaje_descuento)
        self.__componentes = []

    def agregar_componente(self, producto):
        self.__componentes.append(producto)

    def calcular_precio(self):
        total = sum(producto.calcular_precio() for producto in self.__componentes)
        return total * (1 - self.__porcentaje_descuento)

    def obtener_tipo(self):
        return "Combo"
