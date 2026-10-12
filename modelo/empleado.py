from abc import ABC, abstractmethod


class Empleado(ABC):
    def __init__(self, codigo, nombres, dni, sueldo_basico, activo=True):
        self.__codigo = codigo
        self.__nombres = nombres
        self.__dni = dni
        self.__sueldo_basico = float(sueldo_basico)
        self.__activo = activo

    def obtener_codigo(self):
        return self.__codigo

    def obtener_nombres(self):
        return self.__nombres

    def obtener_dni(self):
        return self.__dni

    def obtener_sueldo_basico(self):
        return self.__sueldo_basico

    def esta_activo(self):
        return self.__activo

    @abstractmethod
    def calcular_remuneracion(self):
        pass

    @abstractmethod
    def obtener_tipo(self):
        pass


class Mozo(Empleado):
    def __init__(self, codigo, nombres, dni, sueldo_basico, porcentaje_propina, activo=True):
        super().__init__(codigo, nombres, dni, sueldo_basico, activo)
        self.__porcentaje_propina = float(porcentaje_propina)
        self.__propina_acumulada = 0.0

    def registrar_propina(self, monto):
        self.__propina_acumulada += monto

    def obtener_propina(self):
        return self.__propina_acumulada

    def obtener_propina_acumulada(self):
        return self.__propina_acumulada

    def calcular_remuneracion(self):
        return self.obtener_sueldo_basico() + self.__propina_acumulada * self.__porcentaje_propina

    def obtener_tipo(self):
        return "Mozo"


class Cocinero(Empleado):
    def __init__(self, codigo, nombres, dni, sueldo_basico, especialidad="", activo=True):
        super().__init__(codigo, nombres, dni, sueldo_basico, activo)
        self.__especialidad = especialidad

    def calcular_remuneracion(self):
        return self.obtener_sueldo_basico()

    def obtener_tipo(self):
        return "Cocinero"


class Repartidor(Empleado):
    def __init__(self, codigo, nombres, dni, sueldo_basico, monto_por_entrega, activo=True):
        super().__init__(codigo, nombres, dni, sueldo_basico, activo)
        self.__monto_por_entrega = float(monto_por_entrega)
        self.__entregas_realizadas = 0

    def registrar_entrega(self):
        self.__entregas_realizadas += 1

    def obtener_entregas(self):
        return self.__entregas_realizadas

    def calcular_remuneracion(self):
        return self.obtener_sueldo_basico() + self.__entregas_realizadas * self.__monto_por_entrega

    def obtener_tipo(self):
        return "Repartidor"


class Cajero(Empleado):
    def calcular_remuneracion(self):
        return self.obtener_sueldo_basico()

    def obtener_tipo(self):
        return "Cajero"


class Administrador(Empleado):
    def calcular_remuneracion(self):
        return self.obtener_sueldo_basico()

    def obtener_tipo(self):
        return "Administrador"
