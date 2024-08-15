import datetime

datetime_now: datetime.datetime = datetime.datetime.now()
data_atual: datetime.datetime = datetime.datetime(datetime_now.year, datetime_now.month, datetime_now.day)

class Paciente:
    def __init__(self, nome: str, cpf: str, telefone: str, nascimento: datetime.datetime) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone
        self.__nascimento = nascimento
    
    def idade(self) -> str:
        idade_dias: int = (data_atual - self.__nascimento).days
        idade_anos: int = idade_dias // 365
        idade_meses: int = (idade_dias % 365) // 30
        idade_dias %= 365
        idade_dias %= 30
        return f"{idade_anos} {idade_meses} {idade_dias}"
    
    def __str__(self) -> str:
        return f"Paciente {self.__nome} [{self.__cpf}] ({self.__telefone}) : Idade -> {self.idade()}"