class Frete:
    def __init__(self, distancia: float, peso: float) -> None:
        if distancia < 0 or peso < 0: raise ValueError("Distância e Pesos devem ser positivas!")
        
        self.__distancia = distancia
        self.__peso = peso
    
    def set_distancia(self, nova_distancia: float) -> None:
        if nova_distancia < 0: raise ValueError("Distância deve ser positiva!")

        self.__distancia = nova_distancia

    def set_peso(self, novo_peso: float) -> None:
        if novo_peso < 0: raise ValueError("Peso deve ser positivo!")

        self.__peso = novo_peso
    
    def get_distancia(self) -> float: return self.__distancia

    def get_peso(self) -> float: return self.__peso

    def calc_frete(self) -> float: return self.__distancia * self.__peso / 100

    def __str__(self) -> str: return f"Distância: {self.__distancia} | Peso: {self.__peso}"

f: Frete = Frete(100, 50)

print(f.calc_frete())