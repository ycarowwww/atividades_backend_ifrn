from enum import Enum, IntFlag

class Dias(IntFlag):
    Segunda = 1
    Terca = 2
    Quarta = 4
    Quinta = 8
    Sexta = 16

class Turno(Enum):
    Matutino = 1
    Vespertino = 2
    Noturno = 3
    
class Estagiario:
    def __init__(self, nome: str, cpf: str, telefone: str, dias: Dias, turno: Turno) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone
        self.__dias = dias
        self.__turno = turno
    
    def set_dias(self, dias: Dias) -> None:
        self.__dias ^= dias
    
    def set_turno(self, turno: Turno) -> None:
        self.__turno = turno

    def get_dias(self) -> Dias: return self.__dias

    def get_turno(self) -> Dias: return self.__turno
    
    def __str__(self) -> str:
        return f"Estagiário {self.__nome} [{self.__cpf}] ({self.__telefone}) - {self.__dias} -> {self.__turno}"