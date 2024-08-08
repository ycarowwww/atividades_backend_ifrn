from math import sqrt

class EquacaoIIGrau:
    def __init__(self, coeficiente_a: float, coeficiente_b: float, coeficiente_c: float) -> None:
        if coeficiente_a == 0: raise ValueError("Coeficiente A não pode ser Igual a 0!")
        
        self.__coeficiente_a = coeficiente_a
        self.__coeficiente_b = coeficiente_b
        self.__coeficiente_c = coeficiente_c
    
    def calc_delta(self) -> float: return self.__coeficiente_b ** 2 - 4 * self.__coeficiente_a * self.__coeficiente_c

    def tem_raizes_reais(self) -> bool: return self.calc_delta() >= 0

    def raiz_1(self) -> float | str:
        if not self.tem_raizes_reais():
            return "Não há raízes reais nessa equação."
        
        return (-self.__coeficiente_b + sqrt(self.calc_delta())) / 2 * self.__coeficiente_a

    def raiz_2(self) -> float | str:
        if not self.tem_raizes_reais():
            return "Não há raízes reais nessa equação."
        
        return (-self.__coeficiente_b - sqrt(self.calc_delta())) / 2 * self.__coeficiente_a
    
    def __str__(self) -> str: return f"A: {self.__coeficiente_a} | B: {self.__coeficiente_b} | C: {self.__coeficiente_c} | Delta: {self.calc_delta()}"