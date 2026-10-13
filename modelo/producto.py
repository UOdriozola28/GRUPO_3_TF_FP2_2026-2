from abc import ABC, abstractmethod


class Producto(ABC):

    def __init__(self, codigo, nombre, precio_base):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio_base = precio_base

    def obtener_codigo(self):
        return self.__codigo

    def obtener_nombre(self):
        return self.__nombre

    def obtener_precio_base(self):
        return self.__precio_base

    @abstractmethod
    def obtener_categoria(self):
        pass

    @abstractmethod
    def calcular_precio(self):
        pass

    def __str__(self):
        return f"{self.__codigo} - {self.__nombre} - {self.obtener_categoria()} - S/ {self.calcular_precio():.2f}"


class Bebida(Producto):

    def __init__(self, codigo, nombre, precio_base, presentacion):
        super().__init__(codigo, nombre, precio_base)
        self.__presentacion = presentacion

    def obtener_presentacion(self):
        return self.__presentacion

    def obtener_categoria(self):
        return "Bebida"

    def calcular_precio(self):
        return self.obtener_precio_base()

    def __str__(self):
        return super().__str__() + f" - Presentacion: {self.__presentacion}"


class Plato(Producto):

    def __init__(self, codigo, nombre, precio_base, tamano):
        super().__init__(codigo, nombre, precio_base)
        self.__tamano = tamano

    def obtener_tamano(self):
        return self.__tamano

    def obtener_categoria(self):
        return "Plato"

    def calcular_precio(self):
        precio = self.obtener_precio_base()
        if self.__tamano == "Mediano":
            precio = precio + 3
        if self.__tamano == "Grande":
            precio = precio + 6
        return precio

    def __str__(self):
        return super().__str__() + f" - Tamano: {self.__tamano}"


class Combo(Producto):

    def __init__(self, codigo, nombre, descuento):
        super().__init__(codigo, nombre, 0.0)
        self.__componentes = []
        self.__descuento = descuento

    def obtener_componentes(self):
        return self.__componentes

    def agregar_componente(self, producto):
        self.__componentes.append(producto)

    def calcular_precio(self):
        suma = 0.0
        for componente in self.__componentes:
            suma = suma + componente.calcular_precio()
        descuento_soles = suma * self.__descuento
        return suma - descuento_soles

    def obtener_categoria(self):
        return "Combo"

    def __str__(self):
        return super().__str__() + f" - Componentes: {len(self.__componentes)}"
