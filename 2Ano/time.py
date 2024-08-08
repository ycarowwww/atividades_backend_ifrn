from time import sleep

class Jogador:
    def __init__(self, nome: str, camisa: str, numgols: int) -> None:
        self.__nome = nome
        self.__camisa = camisa
        self.__numgols = numgols
    
    def set_nome(self, novo_nome: str) -> None:
        if not novo_nome: raise Exception("Nome não pode ser Nulo.")
        self.__nome = novo_nome
    
    def set_camisa(self, nova_camisa: str) -> None:
        if not nova_camisa: raise Exception("Camisa não pode ser Nula.")
        self.__camisa = nova_camisa
    
    def set_numgols(self, novo_numgols: int) -> None:
        if novo_numgols < 0: raise Exception("Número de Gols não pode ser Negativo.")
        self.__numgols = novo_numgols
    
    def get_nome(self) -> str: return self.__nome

    def get_camisa(self) -> str: return self.__camisa
    
    def get_numgols(self) -> int: return self.__numgols
    
    def __str__(self) -> str:
        return f"Jogador: {self.__nome} Nº {self.__camisa} | marcou {self.__numgols} gols"

class Time:
    def __init__(self, nome: str, estado: str, jogadores: list[Jogador]) -> None:
        self.__nome = nome
        self.__estado = estado
        self.__jogadores = jogadores
    
    def inserir(self, novo_jogador: Jogador) -> None:
        if novo_jogador in self.__jogadores: raise Exception("Jogador já está inserido na Lista.")
        self.__jogadores.append(novo_jogador)
    
    def listar_jogadores(self) -> list[Jogador]: return self.__jogadores

    def get_artilheiro(self) -> Jogador:
        jogadores_gols: list[int] = []
        for i in self.__jogadores:
            jogadores_gols.append(i.get_numgols())
        return self.__jogadores[jogadores_gols.index(max(jogadores_gols))]
    
    def __str__(self) -> str:
        return f"Time do {self.__estado}: {self.__nome} possui {len(self.__jogadores)} Jogadores"

class UI:
    time: Time = []
    
    @staticmethod
    def menu() -> str:
        print(" 1 - Criar Novo Time \n 2 - Inserir Jogadores \n 3 - Listar Jogadores \n 4 - Mostrar Artilheiro \n 5 - Terminar Programa")
        return input(" - Selecione uma das Opções: ")

    @staticmethod
    def main() -> None:
        opcao: str = UI.menu()

        while opcao != "5":
            if opcao == "1": UI.criar_time()
            elif opcao == "2": UI.inserir_jogadores()
            elif opcao == "3": UI.listar_jogadores()
            elif opcao == "4": UI.mostrar_artilheiro()
            else: print("Opção Inválida!")

            sleep(3)
            print("-" * 50)

            opcao: str = UI.menu()
        
        print("Fim do Programa!")
    
    @staticmethod
    def criar_time() -> None:
        UI.time = Time(input(" - Nome do Time: "), input(" - Estado do Time: "), [])
        print(" - Time Criado com Sucesso!")
    
    @staticmethod
    def inserir_jogadores() -> None:
        UI.time.inserir(Jogador(input(" - Digite o Nome do Jogador: "), input(" - Digite o Número da Camisa: "), int(input(" - Digite o Número de Gols: "))))
        print(" - Jogador Inserido com Sucesso!")
    
    @staticmethod
    def listar_jogadores() -> None:
        print(*[jogador for jogador in UI.time.listar_jogadores()], sep="\n")
        print(" - Jogadores Listado!")
    
    @staticmethod
    def mostrar_artilheiro() -> None:
        print(UI.time.get_artilheiro())
        print(" - Artilheiro Mostrado com Sucesso!")

if __name__ == "__main__":
    UI.main()