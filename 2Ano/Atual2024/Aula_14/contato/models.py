from datetime import datetime
import json
from os.path import exists as path_exists
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
        if new_contact_id < 0: raise ValueError("ID can't be negative.")
        
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
        return f"Contato {self.contact_id} - '{self.name}' : {self.number} - {self.email} - {self.birthday.strftime("%d/%m/%Y")}"

class ContactDAO:
    __objects: list[Contact] = []

    @classmethod
    def append(cls, obj: Contact) -> None:
        cls.__open_file()
        
        new_id: int = 1
        while cls.get_contact(new_id) is not None:
            new_id += 1
        
        obj.contact_id = new_id
        cls.__objects.append(obj)

        cls.__save_file()
        
    @classmethod
    def get_contacts(cls) -> list[Contact]:
        cls.__open_file()
        return cls.__objects

    @classmethod
    def get_contact(cls, searched_id: int) -> Contact | None:
        cls.__open_file()

        for contact in cls.__objects:
            if contact.contact_id == searched_id:
                return contact

    @classmethod
    def update_contact(cls, obj: Contact) -> None:
        cls.__open_file()

        cur_obj = cls.get_contact(obj.contact_id)
        if cur_obj is None: raise ValueError("Passed Contact doesn't exist on database.")

        cur_obj.name = obj.name
        cur_obj.email = obj.email
        cur_obj.number = obj.number
        cur_obj.birthday = obj.birthday

        cls.__save_file()
        
    @classmethod
    def search_by_initial(cls, name_initial: str) -> list[Contact]:
        cls.__open_file()

        contacts_searched: list[Contact] = []
        for contact in cls.__objects:
            if contact.name.lower().startswith(name_initial.lower()):
                contacts_searched.append(contact)
        
        return contacts_searched
        
    @classmethod
    def search_by_birthmonth(cls, month: int) -> list[Contact]:
        cls.__open_file()

        contacts_searched: list[Contact] = []
        for contact in cls.__objects:
            if contact.birthday.month == month:
                contacts_searched.append(contact)
        
        return contacts_searched
        
    @classmethod
    def remove(cls, obj: Contact) -> None:
        cls.__open_file()
        
        cur_obj = cls.get_contact(obj.contact_id)
        if cur_obj is None: raise ValueError("Passed Contact doesn't exist on database.")

        cls.__objects.remove(cur_obj)

        cls.__save_file()

    @classmethod
    def __open_file(cls) -> None:
        cls.__objects = []

        if path_exists("contacts.json"):
            with open("contacts.json", mode="r") as file:
                data: list[dict[str, Any]] = json.load(file)

                for contact in data:
                    birthday = datetime.strptime(contact["birthday"], "%d/%m/%Y")
                    new_obj = Contact(contact["contact_id"], contact["name"], contact["email"], contact["number"], birthday)
                    cls.__objects.append(new_obj)

    @classmethod
    def __save_file(cls) -> None:
        with open("contacts.json", mode="w") as file:
            json.dump(cls.__objects, file, indent=4, default=cls.__get_vars)
        
    @classmethod
    def __get_vars(cls, obj: object) -> dict[str, Any]:
        obj_vars = vars(obj)
        formatted_obj_vars: dict[str, Any] = {}
        for v in obj_vars:
            value = obj_vars[v]
            if isinstance(value, datetime):
                value = value.strftime("%d/%m/%Y")
            formatted_obj_vars[cls.__remove_private(v)] = value
        return formatted_obj_vars
    
    @staticmethod
    def __remove_private(name: str) -> str:
        return name.split("__")[-1]
