from views import View

class UI:
    @staticmethod
    def menu() -> int:
        print(f"{'Menu':^50}")
        print("=" * 50)
        print("1 - Inserir um novo cliente\n2 - Listar todos os clientes\n3 - Atualizar os dados de um cliente\n4 - Excluir um Cliente\n5 - Sair")
        return int(input("- Selecione uma Opção acima: "))

    @staticmethod
    def main() -> None:
        while True:
            opt = UI.menu()

            match opt:
                case 1: UI.append_client()
                case 2: UI.get_client_list()
                case 3: UI.update_client()
                case 4: UI.remove_client()
                case 5:
                    print("Saindo do Programa")
                    break
                case _: print("Opção Inválida!")

    @staticmethod
    def append_client() -> None:
        print(f"{'Inserir Cliente':^50}")
        print("=" * 50)
        name: str = input("- Insira o nome de um Cliente: ")
        email: str = input("- Insira o email de um Cliente: ")
        phone: str = input("- Insira o telefone de um Cliente: ")
        View.append_client(name, email, phone)

        print("Cliente adicionado com Sucesso!")

    @staticmethod
    def get_client_list() -> None:
        print(f"{'Lista de Clientes':^50}")
        print("=" * 50)
        clients = View.get_client_list()

        if len(clients) <= 0:
            print("Não há Clientes!")
            return

        for client in clients:
            print(client)

    @staticmethod
    def update_client() -> None:
        clients = View.get_client_list()
        if len(clients) <= 0:
            print("Não há Clientes!")
            return
        
        UI.get_client_list()
        print("=" * 50)
        print(f"{'Atualizar Cliente':^50}")
        print("=" * 50)
        client_id = int(input("- Insira o ID do Cliente: "))
        name: str = input("- Insira o nome de um Cliente: ")
        email: str = input("- Insira o email de um Cliente: ")
        phone: str = input("- Insira o telefone de um Cliente: ")

        View.update_client(client_id, name, email, phone)

        print("Cliente atualizado com Sucesso!")

    @staticmethod
    def remove_client() -> None:
        clients = View.get_client_list()
        if len(clients) <= 0:
            print("Não há Clientes!")
            return

        UI.get_client_list()
        print("=" * 50)
        print(f"{'Remover Cliente':^50}")
        print("=" * 50)
        client_id = int(input("- Insira o ID do Cliente: "))

        View.remove_client(client_id)

        print("Cliente removido com Sucesso!")

if __name__ == '__main__':
    UI.main()
