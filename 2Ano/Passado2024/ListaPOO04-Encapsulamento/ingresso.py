from time import sleep

class Ingresso:
    def __init__(self, dia: str, hora: int) -> None:
        if hora < 0 or hora > 23: raise ValueError("Hora deve ser entre 0 e 23")
        
        self.__dia = dia
        self.__hora = hora
    
    def get_dia(self) -> str: return self.__dia

    def get_hora(self) -> int: return self.__hora

    def set_dia(self, novo_dia: str) -> None:
        self.__dia = novo_dia
    
    def set_hora(self, nova_hora: int) -> None:
        if nova_hora < 0 or nova_hora > 23: raise ValueError("Hora deve ser entre 0 e 23")

        self.__hora = nova_hora
    
    def valor_ingresso(self) -> float:
        if self.__dia == "quinta-feira": return 6.00
        elif self.__hora <= 16: return 5.00
        else: return 10.00

class UI:
    ingresso: Ingresso | None = None
    
    @staticmethod
    def menu() -> str:
        print(" 1 - Criar Ingresso \n 2 - Ver Dados \n 3 - Definir Dia \n 4 - Definir Hora \n 5 - Valor do Ingresso \n 6 - Sair")
        return input(" - Escolha uma das Opções Acima: ")
    
    @staticmethod
    def main() -> None:
        print(f"{"Ingresso":^50}")
        print("=" * 50)
        opcao: str = ""
        while opcao != "6":
            opcao = UI.menu()
            print("-" * 50)

            match opcao:
                case "1": UI.criar_ingresso()
                case "2": UI.ver_dados()
                case "3": UI.definir_dia()
                case "4": UI.definir_hora()
                case "5": UI.valor_ingresso()
                case "6": print("Obrigado por usar o Programa!")
                case _: print("Opção Inválida!")

            sleep(1)
            print("-" * 50)
    
    @staticmethod
    def criar_ingresso() -> None:
        dia: str = input("- Digite o Dia: ")
        hora: int = int(input("- Digite a Hora: "))
        UI.ingresso = Ingresso(dia, hora)
        print("Ingresso criado com Sucesso!")
    
    @staticmethod
    def ver_dados() -> None:
        if not UI.ingresso:
            print("Ingresso ainda não foi Criado!")
            return

        print(f"Dia: {UI.ingresso.get_dia()}")
        print(f"Hora: {UI.ingresso.get_hora()}")
    
    @staticmethod
    def definir_dia() -> None:
        if not UI.ingresso:
            print("Ingresso ainda não foi Criado!")
            return
        
        novo_dia: str = input("- Digite o Novo Dia: ")
        UI.ingresso.set_dia(novo_dia)
        print("Dia modificado com Sucesso!")
    
    @staticmethod
    def definir_hora() -> None:
        if not UI.ingresso:
            print("Ingresso ainda não foi Criado!")
            return

        nova_hora: int = int(input("- Digite a Nova Hora: "))
        UI.ingresso.set_hora(nova_hora)
        print("Hora modificada com Sucesso!")
    
    @staticmethod
    def valor_ingresso() -> None:
        if not UI.ingresso:
            print("Ingresso ainda não foi Criado!")
            return
        
        print(f"Valor do Ingresso: R${UI.ingresso.valor_ingresso():.2f}")

if __name__ == '__main__':
    UI.main()