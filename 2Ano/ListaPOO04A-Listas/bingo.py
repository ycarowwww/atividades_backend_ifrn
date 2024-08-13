from random import choice

class Bingo:
    def __init__(self) -> None:
        self.__bolas: list[int] = []
        self.__bolas_sorteadas: list[int] = []
    
    def iniciar(self, num_bolas: int) -> None:
        self.__bolas = list(range(1, num_bolas+1))
    
    def proximo(self) -> int:
        self.__bolas_sorteadas.append(choice(self.__bolas))
        self.__bolas.remove(self.__bolas_sorteadas[-1])
        return self.__bolas_sorteadas[-1]

    def sorteados(self) -> list[int]:
        return self.__bolas_sorteadas