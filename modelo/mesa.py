class Mesa:
    def __init__(self, numero, capacidad):
        self.__numero = numero
        self.__capacidad = capacidad
        self.__estado = "Libre"

    def obtener_numero(self):
        return self.__numero

    def obtener_capacidad(self):
        return self.__capacidad

    def obtener_estado(self):
        return self.__estado

    def ocupar(self):
        self.__estado = "Ocupada"

    def liberar(self):
        self.__estado = "Libre"

    def esta_libre(self):
        return self.__estado == "Libre"
