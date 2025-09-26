from datetime import datetime
import json
import os
from typing import Any

def get_file_path(file: str) -> str:
    """Gets the absolute path of a specific file."""
    base_dir: str = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_dir, file)

class Schedule:
    def __init__(self, schedule_id: int, date: datetime, confirmed: bool = False, client_id: int = 0, service_id: int = 0, professional_id: int = 0) -> None:
        self.id = schedule_id
        self.date = date
        self.confirmed = confirmed
        self.client_id = client_id
        self.service_id = service_id
        self.professional_id = professional_id

    @property
    def id(self) -> int: return self.__id

    @id.setter
    def id(self, new_id: int) -> None:
        if not isinstance(new_id, int): raise TypeError("ID needs to be an Integer.")
        if new_id < 0: raise ValueError("ID needs to be greater than Zero.")

        self.__id = new_id

    @property
    def date(self) -> datetime: return self.__date

    @date.setter
    def date(self, new_date: datetime) -> None:
        if not isinstance(new_date, datetime): raise TypeError("Date needs to be a Datetime.")
        if new_date < datetime(1900, 1, 1): raise ValueError("Date too long ago.")

        self.__date = new_date

    @property
    def confirmed(self) -> bool: return self.__confirmed

    @confirmed.setter
    def confirmed(self, new_confirmed: bool) -> None:
        if not isinstance(new_confirmed, bool): raise TypeError("Confirmed needs to be a Boolean.")

        self.__confirmed = new_confirmed

    @property
    def client_id(self) -> int: return self.__client_id

    @client_id.setter
    def client_id(self, new_client_id: int) -> None:
        if not isinstance(new_client_id, int): raise TypeError("Client's ID needs to be an Integer.")
        if new_client_id < 0: raise ValueError("Client's ID needs to be greater than Zero.")

        self.__client_id = new_client_id

    @property
    def service_id(self) -> int: return self.__service_id

    @service_id.setter
    def service_id(self, new_service_id: int) -> None:
        if not isinstance(new_service_id, int): raise TypeError("Service's ID needs to be an Integer.")
        if new_service_id < 0: raise ValueError("Service's ID needs to be greater than Zero.")

        self.__service_id = new_service_id

    @property
    def professional_id(self) -> int: return self.__professional_id

    @professional_id.setter
    def professional_id(self, new_professional_id: int) -> None:
        if not isinstance(new_professional_id, int): raise TypeError("Professional's ID needs to be an Integer.")
        if new_professional_id < 0: raise ValueError("Professional's ID needs to be greater than Zero.")

        self.__professional_id = new_professional_id

    def get_formatted_date(self) -> str: return self.date.strftime("%d/%m/%Y %H:%M:%S")

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date.strftime("%d/%m/%Y %H:%M:%S"),
            "confirmed": self.confirmed,
            "client_id": self.client_id,
            "service_id": self.service_id,
            "professional_id": self.professional_id
        }
    
    @staticmethod
    def from_json(data: dict[str, Any]) -> "Schedule":
        return Schedule(data["id"], datetime.strptime(data["date"], "%d/%m/%Y %H:%M:%S"), data["confirmed"], data["client_id"], data["service_id"], data["professional_id"])

    def __str__(self) -> str:
        available = "Confirmado" if self.confirmed else "Não Confirmado"
        return f"Horário {self.id}: {self.date.strftime("%d/%m/%Y %H:%M:%S")} - {available}"

class ScheduleDAO:
    __objects: list[Schedule] = []
    __json_file_path: str = get_file_path("../data/schedules.json")

    @classmethod
    def append(cls, obj: Schedule) -> None:
        cls.__open_file()
        
        new_id: int = 1
        while cls.get_schedule(new_id) is not None:
            new_id += 1
        
        obj.id = new_id
        cls.__objects.append(obj)

        cls.__save_file()
    
    @classmethod
    def get_schedules(cls) -> list[Schedule]: 
        cls.__open_file()
        return cls.__objects

    @classmethod
    def get_schedule(cls, searched_id: int) -> Schedule | None:
        cls.__open_file()

        for schedule in cls.__objects:
            if schedule.id == searched_id:
                return schedule

    @classmethod
    def update(cls, obj: Schedule) -> None:
        cls.__open_file()

        cur_obj = cls.get_schedule(obj.id)
        if cur_obj is None: raise ValueError("Passed Schedule doesn't exist on database.")

        cur_obj.date = obj.date
        cur_obj.confirmed = obj.confirmed
        cur_obj.client_id = obj.client_id
        cur_obj.service_id = obj.service_id
        cur_obj.professional_id = obj.professional_id

        cls.__save_file()

    @classmethod
    def remove(cls, obj: Schedule) -> None:
        cls.__open_file()
        
        cur_obj = cls.get_schedule(obj.id)
        if cur_obj is None: raise ValueError("Passed Schedule doesn't exist on database.")

        cls.__objects.remove(cur_obj)

        cls.__save_file()

    @classmethod
    def __open_file(cls) -> None:
        cls.__objects = []

        if os.path.exists(cls.__json_file_path):
            with open(cls.__json_file_path, mode="r") as file:
                data: list[dict[str, Any]] = json.load(file)

                for client in data:
                    new_obj = Schedule.from_json(client)
                    cls.__objects.append(new_obj)

    @classmethod
    def __save_file(cls) -> None:
        with open(cls.__json_file_path, mode="w") as file:
            json_objects = [ obj.to_json() for obj in cls.__objects ]
            json.dump(json_objects, file, indent=4)
