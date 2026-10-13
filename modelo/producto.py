from abc import ABC, abstractmethod
class Producto (ABC):
    def __init__ (self, codigo, nombre, precio_base):
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

    def __str__ (self):
        return f"Codigo: {self.__codigo}, Nombre: {self.__nombre}, Precio Base: {self.__precio_base}"

class Bebida(Producto):
    def __init__(self, codigo, nombre, precio_base, presentacion):
        super().__init__(codigo, nombre, precio_base) 
        self.__presetacion = presentacion

    def obtener_presentacion(self):
        return self.__presetacion

    def obtener_categoria(self):
        return "Bebida"
    
    def __str__(self):
            return super().__str__()+ f"Presentacion:  {self.__presetacion}"
    
    def calcular_precio(self):
        return self.obtener_precio_base()

class Plato(Producto):
    def __init__(self, codigo, nombre, precio_base, tamano):
        super().__init__(codigo, nombre, precio_base)
        self.__tamano =  tamano

    def obtener_tamano(self):
        return self.__tamano

    def obtener_categoria(self):
        return "Plato"
    
    def __str__(self):
        return super().__str__()+ f"Tamanio: {self.__tamano}"

    def calcular_precio(self):
        precio= self.obtener_precio_base()
        if self.__tamano == "Mediano":
            precio += 3
        if self.__tamano == "Grande":
            precio += 6
        return precio
    
    
class Combo(Producto):
    def __init__(self, codigo, nombre, precio_base, descuento):
        super().__init__(codigo, nombre, precio_base)
        self.__componentes = []
        self.__descuento = descuento
    
    def obtener_componentes(self):
        return self.__componentes
    
    def agregar_componentes(self, producto):
        self.__componentes.append(producto)

    def calcular_precio(self):
        suma = 0
        for componente in self.__componentes:
            suma += componente.calcular_precio()
        descuento_soles = suma * self.__descuento
        return suma - descuento_soles

    def obtener_categoria(self):
        return "Combo"
    
    
    
    
    
    
    