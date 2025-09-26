import json
import os
from typing import Any

def get_file_path(file: str) -> str:
    """Gets the absolute path of a specific file."""
    base_dir: str = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_dir, file)

class Professional:
    def __init__(self, prof_id: int, name: str, speciality: str, council: str) -> None:
        self.id = prof_id
        self.name = name
        self.speciality = speciality
        self.council = council
    
    @property
    def id(self) -> int: return self.__id

    @id.setter
    def id(self, prof_id: int) -> None:
        if not isinstance(prof_id, int): raise TypeError("ID needs to be an INT.") # type: ignore
        if prof_id < 0: raise ValueError("ID can't be negative.")

        self.__id = prof_id

    @property
    def name(self) -> str: return self.__name

    @name.setter
    def name(self, name: str) -> None:
        name = name.strip()
        if name == "": raise ValueError("Name can't be empty.")

        self.__name = name

    @property
    def speciality(self) -> str: return self.__speciality

    @speciality.setter
    def speciality(self, speciality: str) -> None:
        speciality = speciality.strip()
        if speciality == "": raise ValueError("Speciality can't be empty.")

        self.__speciality = speciality

    @property
    def council(self) -> str: return self.__council

    @council.setter
    def council(self, council: str) -> None:
        council = council.strip()
        if council == "": raise ValueError("Council can't be empty.")

        self.__council = council

    def __str__(self) -> None:
        return f"Profissional {self.id} : {self.name} - {self.speciality} e {self.council}"

    def to_json(self) -> dict[str, Any]:
        """Converts Professional's data to a JSON format."""
        return {
            "prof_id": self.id,
            "name": self.name,
            "speciality": self.speciality,
            "council": self.council
        }

    @staticmethod
    def from_json(data: dict[str, Any]) -> "Professional":
        """Reads JSON format data and converts it to a real Professional object."""
        return Professional(data["prof_id"], data["name"], data["speciality"], data["council"])

class ProfessionalDAO:
    __objects: list[Professional] = []
    __json_file_path: str = get_file_path("../data/professionals.json")

    @classmethod
    def append(cls, obj: Professional) -> None:
        cls.__open_file()
        
        new_id: int = 1
        while cls.get_professional(new_id) is not None:
            new_id += 1
        
        obj.id = new_id
        cls.__objects.append(obj)

        cls.__save_file()
    
    @classmethod
    def get_professionals(cls) -> list[Professional]: 
        cls.__open_file()
        return cls.__objects

    @classmethod
    def get_professional(cls, searched_id: int) -> Professional | None:
        cls.__open_file()

        for professional in cls.__objects:
            if professional.id == searched_id:
                return professional

    @classmethod
    def update(cls, obj: Professional) -> None:
        cls.__open_file()

        cur_obj = cls.get_professional(obj.id)
        if cur_obj is None: raise ValueError("Passed Professional doesn't exist on database.")

        cur_obj.name = obj.name
        cur_obj.speciality = obj.speciality
        cur_obj.council = obj.council

        cls.__save_file()

    @classmethod
    def remove(cls, obj: Professional) -> None:
        cls.__open_file()
        
        cur_obj = cls.get_professional(obj.id)
        if cur_obj is None: raise ValueError("Passed Professional doesn't exist on database.")

        cls.__objects.remove(cur_obj)

        cls.__save_file()

    @classmethod
    def __open_file(cls) -> None:
        cls.__objects = []

        if os.path.exists(cls.__json_file_path):
            with open(cls.__json_file_path, mode="r") as file:
                data: list[dict[str, Any]] = json.load(file)

                for professional in data:
                    new_obj = Professional.from_json(professional)
                    cls.__objects.append(new_obj)

    @classmethod
    def __save_file(cls) -> None:
        with open(cls.__json_file_path, mode="w") as file:
            json_objects = [ obj.to_json() for obj in cls.__objects ]
            json.dump(json_objects, file, indent=4)
