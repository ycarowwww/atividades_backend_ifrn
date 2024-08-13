class Cliente:
    def __init__(self, nome: str, cpf: str, limite: float) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__limite = limite
    
    def get_nome(self) -> str: return self.__nome
    
    def get_cpf(self) -> str: return self.__cpf
    
    def get_limite(self) -> float: return self.__limite
    
    def set_nome(self, novo_nome: str) -> None:
        self.__nome = novo_nome
    
    def set_cpf(self, novo_cpf: str) -> None:
        self.__cpf = novo_cpf
    
    def set_limite(self, novo_limite: float) -> None:
        self.__limite = novo_limite
    
    def __str__(self) -> str:
        return f"Cliente: {self.__nome} [{self.__cpf}] -> R${self.__limite:.2f}"

class Empresa:
    def __init__(self, nome: str, clientes: list[Cliente]) -> None:
        self.__nome = nome
        self.__clientes = clientes
    
    def inserir(self, novo_cliente: Cliente) -> None:
        self.__clientes.append(novo_cliente)
    
    def excluir(self, cliente_index: int) -> None:
        self.__clientes.pop(cliente_index)
    
    def listar(self) -> list[Cliente]:
        return self.__clientes
    
    def total(self) -> float:
        return sum([cliente.get_limite() for cliente in self.__clientes])

    def __str__(self) -> str:
        return f"Empresa {self.__nome} : Quantidade de Clientes - {len(self.__clientes)}"