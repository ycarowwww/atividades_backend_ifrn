from views import View

class UI:
    @classmethod
    def main(cls) -> None:
        while True:
            option: int = cls.menu()
            print("=" * 50)

            match option:
                case 1: cls.append_contact()
                case 2: cls.list_contacts()
                case 3: cls.list_contact_id()
                case 4: cls.update_contact()
                case 5: cls.remove_contact()
                case 6: cls.search_by_initial()
                case 7: cls.search_birthmonth()
                case 8:
                    print("Saindo do Programa...")
                    break
                case _: print("Opção Inválida!")

            print("=" * 50)
    
    @staticmethod
    def menu() -> int:
        print(f"{'Menu':^50}")
        print("=" * 50)
        print("1 - Inserir um novo contato\n2 - Listar todos os contatos\n3 - Listar contato por ID\n4 - Atualizar os dados de um contato\n5 - Excluir um contato\n6 - Pesquisar contato pelo nome\n7 - Aniversariantes\n8 - Sair")
        return int(input("- Escolha uma das opções acima: "))
    
    @staticmethod
    def append_contact() -> None:
        print(f"{'Adicionar Contato':^50}")
        print("-" * 50)
        name = input("Nome do contato: ")
        email = input("Email do contato: ")
        number = input("Número do contato: ")
        birthday = input("Data de Nascimento [DD/MM/YYYY]: ")

        View.append_contact(name, email, number, birthday)

        print("Contato adicionado com Sucesso!")

    @staticmethod
    def list_contacts() -> None:
        print(f"{'Lista de Contatos':^50}")
        print("-" * 50)
        contact_list = View.get_contact_list()
        if len(contact_list) <= 0:
            print("Não há Contatos na lista!")
            return
        
        for cont in contact_list:
            print(cont)
    
    @staticmethod
    def list_contact_id() -> None:
        print(f"{'Contato por ID':^50}")
        print("-" * 50)
        searched_id: int = int(input("- Insira o ID do Contato: "))
        contact = View.get_contact(searched_id)

        if contact is None: print("Contato não Encontrado!")
        else: print(contact)
    
    @classmethod
    def update_contact(cls) -> None:
        if len(View.get_contact_list()) <= 0:
            print("Não há Contatos na lista!")
            return
        
        cls.list_contacts()
        print("-" * 50)
        contact_id = int(input("- Insira o ID do contato a ser atualizado: "))
        new_name = input("- Novo Nome: ")
        new_email = input("- Novo Email: ")
        new_number = input("- Novo Número: ")
        new_birthday = input("- Nova Data de Nascimento [DD/MM/YYYY]: ")

        View.update_contact(contact_id, new_name, new_email, new_number, new_birthday)

        print("Contato Atualizado com Sucesso!")

    @classmethod
    def remove_contact(cls) -> None:
        if len(View.get_contact_list()) <= 0:
            print("Não há Contatos na lista!")
            return
        
        cls.list_contacts()
        print("-" * 50)
        contact_id = int(input("- Insira o ID do contato a ser deletado: "))
        
        View.remove_contact(contact_id)

        print("Contato deletado com sucesso.")

    @staticmethod
    def search_by_initial() -> None:
        print(f"{'Procurar Contato':^50}")
        print("-" * 50)
        name_initial = input("- Iniciais do contato: ")

        print("Contatos Encontrados: ")
        for cont in View.search_by_initial(name_initial):
            print(cont)

    @staticmethod
    def search_birthmonth() -> None:
        print(f"{'Aniversariantes':^50}")
        print("-" * 50)
        month = int(input("- Mês Procurado: "))

        print("Contatos Encontrados: ")
        for cont in View.search_birthmonth(month):
            print(cont)

if __name__ == '__main__':
    UI.main()
