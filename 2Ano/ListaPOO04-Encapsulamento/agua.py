class Agua:
    def __init__(self, mes: int, ano: int, consumo: int) -> None:
        self.__mes = mes
        self.__ano = ano
        self.__consumo = consumo
    
    def get_mes(self) -> int: return self.__mes
    
    def get_ano(self) -> int: return self.__ano
    
    def get_consumo(self) -> int: return self.__consumo

    def set_mes(self, novo_mes: int) -> None:
        if 12 <= novo_mes <= 1: self.__mes = novo_mes
        else: raise ValueError("Mês tem que estar entre 1 e 12.")

    def set_ano(self, novo_ano: int) -> None:
        if isinstance(novo_ano, int): self.__ano = novo_ano
        else: raise ValueError("Ano tem que ser um inteiro!")

    def set_consumo(self, novo_consumo: int) -> None:
        if isinstance(novo_consumo, int): self.__consumo = novo_consumo
        else: raise ValueError("Ano tem que ser um inteiro!")
    
    def valor_conta(self) -> int:
        """Retorna o Valor da Conta de Água."""
        if self.__consumo <= 10: return 38
        elif self.__consumo <= 20: return 38 + 5 * (self.__consumo - 10)
        else: return 88 + 6 * (self.__consumo - 20)
        
# Fazer Classe para UI depois...