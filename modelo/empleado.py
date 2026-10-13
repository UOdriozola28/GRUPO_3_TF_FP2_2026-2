from abc import ABC, abstractmethod


class Empleado(ABC):

    def __init__(self, codigo, nombres, dni, sueldo_basico):
        self.__codigo = codigo
        self.__nombres = nombres
        self.__dni = dni
        self.__sueldo_basico = sueldo_basico

    def obtener_codigo(self):
        return self.__codigo

    def obtener_nombres(self):
        return self.__nombres

    def obtener_dni(self):
        return self.__dni

    def obtener_sueldo_basico(self):
        return self.__sueldo_basico

    @abstractmethod
    def calcular_remuneracion(self):
        pass

    def calcular_variable(self):
        return self.calcular_remuneracion() - self.obtener_sueldo_basico()

    @abstractmethod
    def obtener_tipo(self):
        pass

    def __str__(self):
        return f"{self.__codigo} - {self.__nombres} - DNI {self.__dni} - Sueldo basico S/ {self.__sueldo_basico:.2f}"


class Mozo(Empleado):

    def __init__(self, codigo, nombres, dni, sueldo_basico, porcentaje_propina):
        super().__init__(codigo, nombres, dni, sueldo_basico)
        self.__porcentaje_propina = porcentaje_propina
        self.__propina_acumulada = 0.0

    def registrar_propina(self, monto):
        self.__propina_acumulada = self.__propina_acumulada + monto

    def obtener_propina(self):
        return self.__propina_acumulada

    def calcular_remuneracion(self):
        extra = self.__propina_acumulada * self.__porcentaje_propina
        return self.obtener_sueldo_basico() + extra

    def obtener_tipo(self):
        return "Mozo"

    def __str__(self):
        return (super().__str__()
                + f" - {self.obtener_tipo()} - Propina acumulada S/ {self.__propina_acumulada:.2f}"
                + f" - Remuneracion S/ {self.calcular_remuneracion():.2f}")


class Repartidor(Empleado):

    def __init__(self, codigo, nombres, dni, sueldo_basico, monto_por_entrega):
        super().__init__(codigo, nombres, dni, sueldo_basico)
        self.__monto_por_entrega = monto_por_entrega
        self.__entregas_realizadas = 0

    def obtener_entregas(self):
        return self.__entregas_realizadas

    def registrar_entrega(self):
        self.__entregas_realizadas = self.__entregas_realizadas + 1

    def calcular_remuneracion(self):
        extra = self.__entregas_realizadas * self.__monto_por_entrega
        return self.obtener_sueldo_basico() + extra

    def obtener_tipo(self):
        return "Repartidor"

    def __str__(self):
        return (super().__str__()
                + f" - {self.obtener_tipo()} - Entregas {self.__entregas_realizadas}"
                + f" - Remuneracion S/ {self.calcular_remuneracion():.2f}")


class Cocinero(Empleado):

    def __init__(self, codigo, nombres, dni, sueldo_basico, especialidad):
        super().__init__(codigo, nombres, dni, sueldo_basico)
        self.__especialidad = especialidad

    def obtener_especialidad(self):
        return self.__especialidad

    def calcular_remuneracion(self):
        return self.obtener_sueldo_basico()

    def obtener_tipo(self):
        return "Cocinero"

    def __str__(self):
        return (super().__str__()
                + f" - {self.obtener_tipo()} - Especialidad {self.__especialidad}"
                + f" - Remuneracion S/ {self.calcular_remuneracion():.2f}")
