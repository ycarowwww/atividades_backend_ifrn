import json
import os
from typing import Any

def get_file_path(file: str) -> str:
    """Gets the absolute path of a specific file."""
    base_dir: str = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_dir, file)

class Service:
    def __init__(self, service_id: int, description: str, value: float) -> None:
        self.id = service_id
        self.description = description
        self.value = value
    
    @property
    def id(self) -> int: return self.__id

    @id.setter
    def id(self, service_id: int) -> None:
        if not isinstance(service_id, int): raise TypeError("ID needs to be an INT.") # type: ignore
        if service_id < 0: raise ValueError("ID can't be negative.")

        self.__id = service_id

    @property
    def description(self) -> str: return self.__description

    @description.setter
    def description(self, description: str) -> None:
        description = description.strip()
        if description == "": raise ValueError("Description can't be empty.")

        self.__description = description

    @property
    def value(self) -> float: return self.__value

    @value.setter
    def value(self, value: float) -> None:
        if not isinstance(value, (int, float)): raise TypeError("Value needs to be a Number.") # type: ignore

        self.__value = value

    def __str__(self) -> str:
        return f"Serviço {self.id}: '{self.description}' - {self.value}"

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "value": self.value
        }

    @staticmethod
    def from_json(data: dict[str, Any]) -> "Service":
        return Service(data["id"], data["description"], data["value"])

class ServiceDAO:
    __objects: list[Service] = []
    __json_file_path: str = get_file_path("../data/services.json")

    @classmethod
    def append(cls, obj: Service) -> None:
        cls.__open_file()
        
        new_id: int = 1
        while cls.get_service(new_id) is not None:
            new_id += 1
        
        obj.id = new_id
        cls.__objects.append(obj)

        cls.__save_file()
    
    @classmethod
    def get_services(cls) -> list[Service]: 
        cls.__open_file()
        return cls.__objects

    @classmethod
    def get_service(cls, searched_id: int) -> Service | None:
        cls.__open_file()

        for service in cls.__objects:
            if service.id == searched_id:
                return service

    @classmethod
    def update(cls, obj: Service) -> None:
        cls.__open_file()

        cur_obj = cls.get_service(obj.id)
        if cur_obj is None: raise ValueError("Passed Service doesn't exist on database.")

        cur_obj.description = obj.description
        cur_obj.value = obj.value

        cls.__save_file()

    @classmethod
    def remove(cls, obj: Service) -> None:
        cls.__open_file()
        
        cur_obj = cls.get_service(obj.id)
        if cur_obj is None: raise ValueError("Passed Service doesn't exist on database.")

        cls.__objects.remove(cur_obj)

        cls.__save_file()

    @classmethod
    def __open_file(cls) -> None:
        cls.__objects = []

        if os.path.exists(cls.__json_file_path):
            with open(cls.__json_file_path, mode="r") as file:
                data: list[dict[str, Any]] = json.load(file)

                for service in data:
                    new_obj = Service.from_json(service)
                    cls.__objects.append(new_obj)

    @classmethod
    def __save_file(cls) -> None:
        with open(cls.__json_file_path, mode="w") as file:
            json_objects = [ obj.to_json() for obj in cls.__objects ]
            json.dump(json_objects, file, indent=4)
