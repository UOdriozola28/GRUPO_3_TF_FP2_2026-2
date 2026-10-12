class Empleado:
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

    def calcular_remuneracion(self):
        pass

    def obtener_tipo(self):
        pass

    def __str__(self):
        return f"codigo: {self.__codigo}, nombres: {self.__nombres}, dni: {self.__dni}, sueldo basico: {self.__sueldo_basico}"

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
        return super().__str__() + f" Porcentaje de propina {self.__porcentaje_propina}, propina acumulada {self.obtener_propina()}, remuneración {self.calcular_remuneracion()}, tipo: {self.obtener_tipo()}"

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
        return super().__str__() + f" monto por entregas: {self.__monto_por_entrega}, número de entregas: {self.obtener_entregas()}, remuneración: {self.calcular_remuneracion()} tipo: {self.obtener_tipo()}"

class Cocinero(Empleado):
    def __init__(self, codigo, nombres, dni, sueldo_basico):
        super().__init__(codigo, nombres, dni, sueldo_basico)

    def calcular_remuneracion(self):
        return self.obtener_sueldo_basico()

    def obtener_tipo(self):
        return "Cocinero"

    def __str__(self):
        return super().__str__() + f" remuneración: {self.calcular_remuneracion()}, tipo: {self.obtener_tipo()}"



