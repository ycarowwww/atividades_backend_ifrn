from .abc_dao import AbstractDAO
from .utils_crypto import Crypto, CryptoBase64
import json
import os
from typing import Any

class Professional:
    def __init__(self, prof_id: int, name: str, email: str, speciality: str, council: str, password: str, services_id: list[int], profile_photo: bytes) -> None:
        self.id = prof_id
        self.name = name
        self.email = email
        self.speciality = speciality
        self.council = council
        self.password = password
        self.services_id = services_id
        self.profile_photo = profile_photo
    
    @property
    def id(self) -> int: return self.__id

    @id.setter
    def id(self, prof_id: int) -> None:
        if not isinstance(prof_id, int): raise TypeError("ID precisa ser um Inteiro.")
        if prof_id < 0: raise ValueError("ID não pode ser negativo.")

        self.__id = prof_id

    @property
    def name(self) -> str: return self.__name

    @name.setter
    def name(self, name: str) -> None:
        name = name.strip()
        if name == "": raise ValueError("Nome não pode ser vazio.")

        self.__name = name

    @property
    def email(self) -> str: return self.__email

    @email.setter
    def email(self, email: str) -> None:
        email = email.strip()
        if email == "": raise ValueError("Email não pode ser vazio.")

        self.__email = email

    @property
    def speciality(self) -> str: return self.__speciality

    @speciality.setter
    def speciality(self, speciality: str) -> None:
        speciality = speciality.strip()
        if speciality == "": raise ValueError("Especialidade não pode ser vazio.")

        self.__speciality = speciality

    @property
    def council(self) -> str: return self.__council

    @council.setter
    def council(self, council: str) -> None:
        council = council.strip()
        if council == "": raise ValueError("Conselho não pode ser vazio.")

        self.__council = council

    @property
    def password(self) -> str:
        return self.__password
    
    @password.setter
    def password(self, new_password: str) -> None:
        new_password = new_password.strip()
        if new_password == "": raise ValueError("Senha não pode ser vazio.")
        
        self.__password = new_password

    @property
    def profile_photo(self) -> bytes:
        return self.__profile_photo
    
    @profile_photo.setter
    def profile_photo(self, new_profile_photo: bytes) -> None:
        if new_profile_photo is None: raise ValueError("Foto de Perfil não pode ser vazio.")
        
        self.__profile_photo = new_profile_photo

    @property
    def services_id(self) -> list[int]:
        return self.__services_id
    
    @services_id.setter
    def services_id(self, new_services_id: list[int]) -> None:
        self.__services_id = new_services_id

    def __str__(self) -> str:
        return f"Profissional {self.id} : {self.name} - {self.speciality} e {self.council}"

    def to_json(self) -> dict[str, Any]:
        """Converte os dados do Objeto para JSON."""
        return {
            "prof_id": self.id,
            "name": self.name,
            "email": self.email,
            "speciality": self.speciality,
            "council": self.council,
            "password": self.password,
            "services_id": self.services_id,
            "profile_photo": self.profile_photo
        }

    @staticmethod
    def from_json(data: dict[str, Any]) -> "Professional":
        """Ler dados JSON e converte para um Objeto dessa Classe."""
        return Professional(data["prof_id"], data["name"], data["email"], data["speciality"], data["council"], data["password"], data["services_id"], data["profile_photo"])

class ProfessionalDAO(AbstractDAO):
    _objects: list[Professional] = []
    _json_file_path_str: str = "../data/professionals.json"
    _from_json_method = Professional.from_json

    @classmethod
    def _open_file(cls) -> None: # Reescrevemos esses dois métodos para tratar a criptografia de alguns dados de seus modelos.
        cls._objects = []

        if os.path.exists(cls._json_file_path):
            with open(cls._json_file_path, mode="r") as file:
                data: list[dict[str, Any]] = json.load(file)

                for obj in data:
                    obj["email"] = Crypto.decrypt(obj["email"])
                    obj["password"] = Crypto.decrypt(obj["password"])
                    obj["profile_photo"] = CryptoBase64.decrypt(obj["profile_photo"])
                    new_obj = cls._from_json_method(obj)
                    cls._objects.append(new_obj)

    @classmethod
    def _save_file(cls) -> None:
        with open(cls._json_file_path, mode="w") as file:
            json_objects: list[dict[str, Any]] = []
            for obj in cls._objects:
                obj_dict = obj.to_json()
                obj_dict["email"] = Crypto.encrypt(obj_dict["email"])
                obj_dict["password"] = Crypto.encrypt(obj_dict["password"])
                obj_dict["profile_photo"] = CryptoBase64.encrypt(obj_dict["profile_photo"])
                json_objects.append(obj_dict)
            json.dump(json_objects, file, indent=4)
