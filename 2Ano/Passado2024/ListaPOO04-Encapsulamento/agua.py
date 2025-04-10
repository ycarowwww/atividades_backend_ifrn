from time import sleep

class Agua:
    def __init__(self, mes: int, ano: int, consumo: int) -> None:
        if mes < 1 or mes > 12: raise ValueError("Mês tem que estar entre 1 e 12.")
        if not isinstance(ano, int): raise ValueError("Ano tem que ser um inteiro!")
        if not isinstance(consumo, int): raise ValueError("Consumo tem que ser um inteiro!")
        self.__mes = mes
        self.__ano = ano
        self.__consumo = consumo
    
    def get_mes(self) -> int: return self.__mes
    
    def get_ano(self) -> int: return self.__ano
    
    def get_consumo(self) -> int: return self.__consumo

    def set_mes(self, novo_mes: int) -> None:
        if 1 <= novo_mes <= 12: self.__mes = novo_mes
        else: raise ValueError("Mês tem que estar entre 1 e 12.")

    def set_ano(self, novo_ano: int) -> None:
        if isinstance(novo_ano, int): self.__ano = novo_ano
        else: raise ValueError("Ano tem que ser um inteiro!")

    def set_consumo(self, novo_consumo: int) -> None:
        if isinstance(novo_consumo, int): self.__consumo = novo_consumo
        else: raise ValueError("Consumo tem que ser um inteiro!")
    
    def valor_conta(self) -> int:
        """Retorna o Valor da Conta de Água."""
        if self.__consumo <= 10: return 38
        elif self.__consumo <= 20: return 38 + 5 * (self.__consumo - 10)
        else: return 88 + 6 * (self.__consumo - 20)
    
    def data_conta(self) -> str: return f"Conta de {self.__consumo}L: {self.__mes:>02}/{self.__ano}"
        
class UI:
    conta: Agua | None = None
    
    @staticmethod
    def menu() -> str:
        print(" 1 - Criar uma Nova Conta \n 2 - Mudar o Mês \n 3 - Mudar o Ano \n 4 - Mudar o Consumo [L] \n 5 - Analisar os Dados \n 6 - Ver o Valor da Conta \n 7 - Sair")
        return input(" - Selecione uma das opções: ")
    
    @staticmethod
    def main() -> None:
        print(f"\033[36m{"Conta de Água!":^50}\033[m")
        print("=" * 50)
        opcao: str = ""
        while opcao != "7":
            opcao = UI.menu()
            print("=" * 50)

            match opcao:
                case "1": UI.nova_conta()
                case "2": UI.mudar_mes()
                case "3": UI.mudar_ano()
                case "4": UI.mudar_consumo()
                case "5": UI.analisar_dados()
                case "6": UI.valor_conta()
                case "7": print("- Obrigado por usar o Programa!")
                case _: print("\033[31mOpção Inválida\033[m")

            sleep(1)
            print("=" * 50)
    
    @staticmethod
    def nova_conta() -> None:
        mes: int = int(input("Digite o mês da Conta: "))
        ano: int = int(input("Digite o ano da Conta: "))
        consumo: int = int(input("Digite o consumo da Conta [L]: "))

        UI.conta = Agua(mes, ano, consumo)

        print("Conta criada com Sucesso!")
    
    @staticmethod
    def mudar_mes() -> None:
        if not UI.conta:
            print("Não é possível alterar dados de uma conta inexistente.")
            return
        
        novo_mes: int = int(input("Digite o novo mês: "))
        UI.conta.set_mes(novo_mes)
    
    @staticmethod
    def mudar_ano() -> None:
        if not UI.conta:
            print("Não é possível alterar dados de uma conta inexistente.")
            return
        
        novo_ano: int = int(input("Digite o novo ano: "))
        UI.conta.set_ano(novo_ano)
    
    @staticmethod
    def mudar_consumo() -> None:
        if not UI.conta:
            print("Não é possível alterar dados de uma conta inexistente.")
            return
        
        novo_consumo: int = int(input("Digite o novo consumo [L]: "))
        UI.conta.set_consumo(novo_consumo)
    
    @staticmethod
    def analisar_dados() -> None:
        if not UI.conta:
            print("Não é possível pegar dados de uma conta inexistente.")
            return

        print(UI.conta.data_conta())
    
    @staticmethod
    def valor_conta() -> None:
        if not UI.conta:
            print("Não é possível pegar dados de uma conta inexistente.")
            return
        
        print(f"Valor da Conta: {UI.conta.valor_conta()}")

if __name__ == "__main__":
    UI.main()