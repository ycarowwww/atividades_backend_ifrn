from datetime import datetime
import json
from os.path import isfile
from typing import Any

class Contact:
    def __init__(self, contact_id: int, name: str, email: str, number: str, birthday: datetime) -> None:
        self.contact_id = contact_id
        self.name = name
        self.email = email
        self.number = number
        self.birthday = birthday

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

    @property
    def birthday(self) -> datetime: return self.__birthday

    @birthday.setter
    def birthday(self, new_birthday: datetime) -> None:
        if new_birthday.year <= 1900: raise ValueError("Invalid Date.")

        self.__birthday = new_birthday

    def __str__(self) -> str:
        return f"{self.contact_id} - '{self.name}' : {self.number} - {self.email} - {self.birthday.strftime("%d/%m/%Y")}"

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
    
    def search_birthmonth(self, month: int) -> list[Contact]:
        contacts_searched: list[Contact] = []
        for cont in self.contacts:
            if cont.birthday.month == month:
                contacts_searched.append(cont)
                
        return contacts_searched

    def append(self, new_contact: Contact) -> None:
        if self.search_id(new_contact.contact_id) is not None: raise ValueError("Contacts cannot have the same id.")
        
        self.contacts.append(new_contact)
        self.contacts.sort(key=lambda c: c.contact_id)
    
    def update(self, contact_id: int, new_name: str = "", new_email: str = "", new_number: str = "", new_birthday: datetime | None = None) -> None:
        contact: Contact | None = self.search_id(contact_id)
        if contact is None: raise ValueError("Unknown Contact ID.")

        new_name = new_name.strip()
        new_email = new_email.strip()
        new_number = new_number.strip()

        if new_name != "": contact.name = new_name
        if new_email != "": contact.email = new_email
        if new_number != "": contact.number = new_number
        if new_birthday is not None: contact.birthday = new_birthday
    
    def remove(self, contact_id: int) -> None:
        contact = self.search_id(contact_id)
        if contact is None: raise ValueError("Contact not in the list.")
        
        self.contacts.remove(contact)

    def clear(self) -> None:
        self.contacts.clear()

class UI:
    __contact_list = ContactList()
    __current_id = 0
    
    @classmethod
    def main(cls) -> None:
        while True:
            option: int = cls.menu()
            print("=" * 50)

            match option:
                case 1: cls.insert_contact()
                case 2: cls.list_contacts()
                case 3: cls.list_contact_id()
                case 4: cls.update_contact()
                case 5: cls.remove_contact()
                case 6: cls.search_contact()
                case 7: cls.search_birthmonth()
                case 8: cls.open_file()
                case 9: cls.save_file()
                case 10:
                    print("Saindo do Programa...")
                    break
                case _:
                    print("Opção Inválida!")

            print("=" * 50)
    
    @staticmethod
    def menu() -> int:
        print(f"{'Menu':^50}")
        print("=" * 50)
        print("1 - Inserir um novo contato\n2 - Listar todos os contatos\n3 - Listar contato por ID\n4 - Atualizar os dados de um contato\n5 - Excluir um contato\n6 - Pesquisar contato pelo nome\n7 - Aniversariantes\n8 - Abrir Arquivo\n9 - Salvar Arquivo\n10 - Sair")
        return int(input("- Escolha uma das opções acima: "))
    
    @classmethod
    def insert_contact(cls) -> None:
        print(f"{'Adicionar Contato':^50}")
        print("-" * 50)
        new_name = input("Nome do contato: ")
        new_email = input("Email do contato: ")
        new_number = input("Número do contato: ")
        new_birthday = datetime.strptime(input("Data de Nascimento [DD/MM/YYYY]: "), "%d/%m/%Y")

        cls.__contact_list.append(Contact(cls.__current_id, new_name, new_email, new_number, new_birthday))
        cls.__current_id += 1

    @classmethod
    def list_contacts(cls) -> None:
        print(f"{'Lista de Contatos':^50}")
        print("-" * 50)
        for cont in cls.__contact_list.contacts:
            print(cont)
    
    @classmethod
    def list_contact_id(cls) -> None:
        print(f"{'Contato por ID':^50}")
        print("-" * 50)
        searched_id: int = int(input("- Insira o ID do Contato: "))
        for cont in cls.__contact_list.contacts:
            if cont.contact_id == searched_id:
                print(cont)
                break
        else:
            print("Contato não encontrado!")
    
    @classmethod
    def update_contact(cls) -> None:
        cls.list_contacts()
        print("-" * 50)
        contact_id = int(input("- Insira o ID do contato a ser atualizado: "))
        print("Insira os novos dados (deixe em branco caso não deseje alterar):")
        new_name = input("Novo Nome: ")
        new_email = input("Novo Email: ")
        new_number = input("Novo Número: ")
        new_birthday = datetime.strptime(input("Nova Data de Nascimento [DD/MM/YYYY]: "), "%d/%m/%Y")
        cls.__contact_list.update(contact_id, new_name, new_email, new_number, new_birthday)
        print("Contato Atualizado com Sucesso!")

    @classmethod
    def remove_contact(cls) -> None:
        cls.list_contacts()
        print("-" * 50)
        contact_id = int(input("- Insira o ID do contato a ser deletado: "))
        cls.__contact_list.remove(contact_id)
        print("Contato deletado com sucesso.")

    @classmethod
    def search_contact(cls) -> None:
        print(f"{'Procurar Contato':^50}")
        print("-" * 50)
        word_starting = input("- Iniciais do contato: ")
        contacts = cls.__contact_list.search_name(word_starting)

        print("Contatos Encontrados: ")
        for cont in contacts:
            print(cont)

    @classmethod
    def search_birthmonth(cls) -> None:
        print(f"{'Aniversariantes':^50}")
        print("-" * 50)
        month = int(input("- Mês Procurado: "))
        contacts = cls.__contact_list.search_birthmonth(month)

        print("Contatos Encontrados: ")
        for cont in contacts:
            print(cont)

    @classmethod
    def open_file(cls) -> None:
        print(f"{'Abrir Arquivo':^50}")
        print("-" * 50)
        file_name: str = input("- Nome do arquivo JSON: ").strip()
        if not isfile(f"{file_name}.json"): 
            print("Arquivo não encontrado!")
            return

        with open(f"{file_name}.json", "r") as json_file:
            contacts_data: list[dict[str, Any]] = json.load(json_file)
            cls.__contact_list.clear()
            cls.__current_id = 0

            for cont in contacts_data:
                new_contact: Contact = Contact(cont["id"], cont["name"], cont["email"], cont["number"], datetime.strptime(cont["birthday"], "%d/%m/%Y"))
                cls.__current_id = max(cls.__current_id, new_contact.contact_id)
                cls.__contact_list.append(new_contact)

            print("Arquivo carregado com sucesso!")

    @classmethod
    def save_file(cls) -> None:
        print(f"{'Salvar Arquivo':^50}")
        print("-" * 50)
        file_name: str = input("- Nome do arquivo JSON ['None' para interromper]: ").strip()
        if file_name == "None" or any(i in file_name for i in ".,#$/\\()[]{}<>:;") or isfile(f"{file_name}.json"): return
        
        contacts: list[Contact] = cls.__contact_list.contacts
        contacts_data: list[dict[str, Any]] = [
            {
                "id" : cont.contact_id,
                "name" : cont.name,
                "email" : cont.email,
                "number" : cont.number,
                "birthday" : cont.birthday.strftime("%d/%m/%Y")
            } 
            for cont in contacts
        ]
        
        with open(f"{file_name}.json", "w") as json_file:
            json.dump(contacts_data, json_file, indent=4)
            print("Arquivo gravado com sucesso!")

if __name__ == "__main__":
    UI.main()
