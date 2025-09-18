import json
import os
from typing import Any

def get_file_path(file: str) -> str:
    """Gets the absolute path of a specific file."""
    base_dir: str = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_dir, file)

class Client:
    def __init__(self, client_id: int, name: str, email: str, phone: str) -> None:
        self.id = client_id
        self.name = name
        self.email = email
        self.phone = phone
    
    @property
    def id(self) -> int: return self.__id

    @id.setter
    def id(self, client_id: int) -> None:
        if not isinstance(client_id, int): raise TypeError("ID needs to be an INT.") # type: ignore
        if client_id < 0: raise ValueError("ID can't be negative.")

        self.__id = client_id

    @property
    def name(self) -> str: return self.__name

    @name.setter
    def name(self, name: str) -> None:
        name = name.strip()
        if name == "": raise ValueError("Name can't be empty.")

        self.__name = name

    @property
    def email(self) -> str: return self.__email

    @email.setter
    def email(self, email: str) -> None:
        email = email.strip()
        if email == "": raise ValueError("Email can't be empty.")

        self.__email = email

    @property
    def phone(self) -> str: return self.__phone

    @phone.setter
    def phone(self, phone: str) -> None:
        phone = phone.strip()
        if phone == "": raise ValueError("Phone can't be empty.")

        self.__phone = phone

    def __str__(self) -> str:
        return f"Cliente {self.id} : {self.name} -> {self.email} | {self.phone}"

    def to_json(self) -> dict[str, Any]:
        """Converts Client's data to a JSON format."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

    @staticmethod
    def from_json(data: dict[str, Any]) -> "Client":
        """Reads JSON format data and converts it to a real Client object."""
        return Client(data["id"], data["name"], data["email"], data["phone"])

class ClientDAO:
    __objects: list[Client] = []
    __json_file_path: str = get_file_path("../data/clients.json")

    @classmethod
    def append(cls, obj: Client) -> None:
        cls.__open_file()
        
        new_id: int = 1
        while cls.get_client(new_id) is not None:
            new_id += 1
        
        obj.id = new_id
        cls.__objects.append(obj)

        cls.__save_file()
    
    @classmethod
    def get_clients(cls) -> list[Client]: 
        cls.__open_file()
        return cls.__objects

    @classmethod
    def get_client(cls, searched_id: int) -> Client | None:
        cls.__open_file()

        for client in cls.__objects:
            if client.id == searched_id:
                return client

    @classmethod
    def update(cls, obj: Client) -> None:
        cls.__open_file()

        cur_obj = cls.get_client(obj.id)
        if cur_obj is None: raise ValueError("Passed Client doesn't exist on database.")

        cur_obj.name = obj.name
        cur_obj.email = obj.email
        cur_obj.phone = obj.phone

        cls.__save_file()

    @classmethod
    def remove(cls, obj: Client) -> None:
        cls.__open_file()
        
        cur_obj = cls.get_client(obj.id)
        if cur_obj is None: raise ValueError("Passed Client doesn't exist on database.")

        cls.__objects.remove(cur_obj)

        cls.__save_file()

    @classmethod
    def __open_file(cls) -> None:
        cls.__objects = []

        if os.path.exists(cls.__json_file_path):
            with open(cls.__json_file_path, mode="r") as file:
                data: list[dict[str, Any]] = json.load(file)

                for client in data:
                    new_obj = Client.from_json(client)
                    cls.__objects.append(new_obj)

    @classmethod
    def __save_file(cls) -> None:
        with open(cls.__json_file_path, mode="w") as file:
            json_objects = [ o.to_json() for o in cls.__objects ]
            json.dump(json_objects, file, indent=4)
