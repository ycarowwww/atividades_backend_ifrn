from time import sleep

class Esporte:
    def __init__(self, nome: str, horarios: str, mensalidade: float) -> None:
        self.__nome = nome
        self.__horarios = horarios
        self.__mensalidade = mensalidade
    
    def get_mensalidade(self) -> float: return self.__mensalidade
    
    def __str__(self) -> str:
        return f"Esporte {self.__nome} {self.__horarios} | R${self.__mensalidade:.2f}"

class Academia:
    def __init__(self, nome: str, endereco: str, esportes: list[Esporte]) -> None:
        self.__nome = nome
        self.__endereco = endereco
        self.__esportes = esportes

    def inserir(self, e: Esporte) -> None:
        self.__esportes.append(e)
    
    def listar(self) -> list[Esporte]: return self.__esportes

    def media_mensalidade(self) -> float:
        media: float = 0
        for esporte in self.__esportes:
            media += esporte.get_mensalidade()
        media /= len(self.__esportes)
        return media

    def __str__(self) -> str:
        return f"Academia {self.__nome} em {self.__endereco} : Possui {len(self.__esportes)} Esportes"

class UI:
    academia: Academia | None = None
    
    @staticmethod
    def menu() -> str:
        print(" 1 - Criar Academia \n 2 - Adicionar Esporte \n 3 - Listar Esportes \n 4 - Média da Mensalidade \n 5 - Informações da Academia \n 6 - Sair do Programa")
        return input(" - Escolha uma das Opções Acima: ")

    @staticmethod
    def main() -> None:
        print(f"{"Crie a sua Academia!":^50}")
        print("=" * 50)
        opcao_atual: str = ""

        while opcao_atual != "6":
            opcao_atual = UI.menu()

            print("-" * 50)
            match opcao_atual:
                case "1": UI.criar_academia()
                case "2": UI.adicionar_esporte()
                case "3": UI.listar_esportes()
                case "4": UI.media_esportes()
                case "5": UI.informacoes_academia()
                case "6": print("Obrigado por usar o Programa!")
                case _: print("Opção Inválida")
            
            sleep(1)
            print("=" * 50)
    
    @staticmethod
    def criar_academia() -> None:
        nome: str = input("- Digite o Nome da Academia: ")
        endereco: str = input("- Digite o Endereço da Academia: ")
        UI.academia = Academia(nome, endereco, [])

        print("Academia criada com Sucesso!")
    
    @staticmethod
    def adicionar_esporte() -> None:
        if not UI.academia:
            print("Crie uma academia primeiro!")
            return

        nome: str = input("- Digite o nome do Esporte: ")
        horarios: str = input("- Digite os horários do Esporte: ")
        mensalidade: float = float(input("- Digite a mensalidade do Esporte: "))
        novo_esporte: Esporte = Esporte(nome, horarios, mensalidade)

        UI.academia.inserir(novo_esporte)

        print("Esporte inserido com Sucesso!")
    
    @staticmethod
    def listar_esportes() -> None:
        if not UI.academia:
            print("Crie uma academia primeiro!")
            return
        elif len(UI.academia.listar()) <= 0:
            print("Há 0 esportes na Academia")
            return
        
        esportes: list[Esporte] = UI.academia.listar()

        for esporte in esportes:
            print(esporte)
    
    @staticmethod
    def media_esportes() -> None:
        if not UI.academia:
            print("Crie uma academia primeiro!")
            return
        
        print(f"Média das Mensalidades: R${UI.academia.media_mensalidade():.2f}")
    
    @staticmethod
    def informacoes_academia() -> None:
        if not UI.academia:
            print("Crie uma academia primeiro!")
            return
        
        print(UI.academia)

if __name__ == '__main__':
    UI.main()