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
        if self.__estado == "Libre":
            return True
        else:
            return False

    def __str__(self):
        return f"Mesa {self.__numero} - Capacidad {self.__capacidad} - {self.__estado}"
