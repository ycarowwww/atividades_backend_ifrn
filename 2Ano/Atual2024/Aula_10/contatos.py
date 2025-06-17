class Contact:
    def __init__(self, contact_id: int, name: str, email: str, number: str) -> None:
        self.contact_id = contact_id
        self.name = name
        self.email = email
        self.number = number

    @property
    def contact_id(self) -> int: return self.__contact_id
    
    @contact_id.setter
    def contact_id(self, new_contact_id: int) -> None:
        if not isinstance(new_contact_id, int): raise TypeError("ID needs to be an int.") # type: ignore
        if new_contact_id < 0: raise ValueError("ID needs to be positive.")
        
        self.__contact_id = new_contact_id
    
    @property
    def name(self) -> str: return self.__name
    
    @name.setter
    def name(self, new_name: str) -> None:
        new_name = new_name.strip()
        if new_name == "": raise ValueError("Name cannot be empty.")
        
        self.__name = new_name
    
    @property
    def email(self) -> str: return self.__email
    
    @email.setter
    def email(self, new_email: str) -> None:
        new_email = new_email.strip()
        if new_email == "": raise ValueError("Email cannot be empty.")
        if new_email.count("@") == 0: raise ValueError("Value needs to be an email.")
        
        self.__email = new_email
    
    @property
    def number(self) -> str: return self.__number
    
    @number.setter
    def number(self, new_number: str) -> None:
        new_number = new_number.strip()
        if new_number == "": raise ValueError("Number cannot be empty.")
        
        self.__number = new_number

    def __str__(self) -> str:
        return f"{self.contact_id} - '{self.name}' : {self.number} - {self.email}"

class ContactList:
    def __init__(self, contacts: list[Contact] = []) -> None:
        self.__contacts = contacts
    
    @property
    def contacts(self) -> list[Contact]: return self.__contacts
    
    def search_id(self, contact_id: int) -> Contact | None:
        for cont in self.contacts:
            if cont.contact_id == contact_id:
                return cont
                
        return None
    
    def search_name(self, contact_name: str) -> list[Contact]:
        contacts_searched: list[Contact] = []
        for cont in self.contacts:
            if cont.name.lower().startswith(contact_name.lower()):
                contacts_searched.append(cont)
                
        return contacts_searched
    
    def append(self, new_contact: Contact) -> None:
        if self.search_id(new_contact.contact_id) is not None: raise ValueError("Contacts cannot have the same id.")
        
        self.contacts.append(new_contact)
        self.contacts.sort(key=lambda c: c.contact_id)
    
    def update(self, contact_id: int, new_name: str = "", new_email: str = "", new_number: str = "") -> None:
        contact: Contact | None = self.search_id(contact_id)
        if contact is None: raise ValueError("Unknown Contact ID.")

        new_name = new_name.strip()
        new_email = new_email.strip()
        new_number = new_number.strip()

        if new_name != "": contact.name = new_name
        if new_email != "": contact.email = new_email
        if new_number != "": contact.number = new_number
    
    def remove(self, contact_id: int) -> None:
        contact = self.search_id(contact_id)
        if contact is None: raise ValueError("Contact not in the list.")
        
        self.contacts.remove(contact)

class UI:
    contact_list = ContactList()
    current_id = 0
    
    @staticmethod
    def main() -> None:
        while True:
            option: int = UI.menu()
            print("=" * 50)

            match option:
                case 1: UI.insert_contact()
                case 2: UI.list_contacts()
                case 3: UI.update_contact()
                case 4: UI.remove_contact()
                case 5: UI.search_contact()
                case 6:
                    print("Saindo do Programa...")
                    return
                case _:
                    print("Opção Inválida!")

            print("=" * 50)
    
    @staticmethod
    def menu() -> int:
        print(f"{'Menu':^50}")
        print("=" * 50)
        print("1 - Inserir um novo contato\n2 - Listar todos os contatos\n3 - Atualizar os dados de um contato\n4 - Excluir um contato\n5 - Pesquisar contato pelo nome\n6 - Sair")
        return int(input("- Escolha uma das opções acima: "))
    
    @staticmethod
    def insert_contact() -> None:
        print(f"{'Adicionar Contato':^50}")
        print("-" * 50)
        new_name = input("Nome do contato: ")
        new_email = input("Email do contato: ")
        new_number = input("Número do contato: ")

        UI.contact_list.append(Contact(UI.current_id, new_name, new_email, new_number))
        UI.current_id += 1

    @staticmethod
    def list_contacts() -> None:
        print(f"{'Lista de Contatos':^50}")
        print("-" * 50)
        for cont in UI.contact_list.contacts:
            print(cont)
    
    @staticmethod
    def update_contact() -> None:
        UI.list_contacts()
        print("-" * 50)
        contact_id = int(input("- Insira o ID do contato a ser atualizado: "))
        print("Insira os novos dados (deixe em branco caso não deseje alterar):")
        new_name = input("Novo Nome: ")
        new_email = input("Novo Email: ")
        new_number = input("Novo Número: ")
        UI.contact_list.update(contact_id, new_name, new_email, new_number)
        print("Contato Atualizado com Sucesso!")

    @staticmethod
    def remove_contact() -> None:
        UI.list_contacts()
        print("-" * 50)
        contact_id = int(input("- Insira o ID do contato a ser deletado: "))
        UI.contact_list.remove(contact_id)
        print("Contato deletado com sucesso.")

    @staticmethod
    def search_contact() -> None:
        print(f"{'Procurar Contato':^50}")
        print("-" * 50)
        word_starting = input("- Iniciais do contato: ")
        contacts = UI.contact_list.search_name(word_starting)

        print("Contatos Encontrados: ")
        for cont in contacts:
            print(cont)

if __name__ == "__main__":
    UI.main()
