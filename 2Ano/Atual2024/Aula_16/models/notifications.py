from .abc_dao import AbstractDAO
from .users_id import UsersTypeIDs
from datetime import datetime
from typing import Any

class Notification:
    def __init__(self, notif_id: int, message: str, date_sent: datetime, receiver_id: int, receiver_type: UsersTypeIDs) -> None:
        self.id = notif_id
        self.message = message
        self.date_sent = date_sent
        self.receiver_id = receiver_id
        self.receiver_type = receiver_type
    
    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, new_id: int) -> None:
        if new_id < 0: raise ValueError("ID não pode ser negativo.")
        
        self.__id = new_id
    
    @property
    def message(self) -> str:
        return self.__message
    
    @message.setter
    def message(self, new_message: str) -> None:
        new_message = new_message.strip()
        if new_message == "": raise ValueError("Mensagem não pode ser vazio.")
        
        self.__message = new_message
    
    @property
    def date_sent(self) -> datetime:
        return self.__date_sent
    
    @date_sent.setter
    def date_sent(self, new_date_sent: datetime) -> None:
        if new_date_sent < datetime(2025, 1, 1): raise ValueError("Data muito antiga.")
        
        self.__date_sent = new_date_sent

    @property
    def receiver_id(self) -> int:
        return self.__receiver_id
    
    @receiver_id.setter
    def receiver_id(self, new_receiver_id: int) -> None:
        if new_receiver_id < 0: raise ValueError("ID não pode ser negativo.")
        
        self.__receiver_id = new_receiver_id
    
    @property
    def receiver_type(self) -> UsersTypeIDs:
        return self.__receiver_type
    
    @receiver_type.setter
    def receiver_type(self, new_receiver_type: UsersTypeIDs) -> None:
        if new_receiver_type not in [ UsersTypeIDs.CLIENT, UsersTypeIDs.PROFESSIONAL ]: raise ValueError("Tipo de Usuário Inválido.")
        
        self.__receiver_type = new_receiver_type
    
    def get_formatted_date_sent(self) -> str:
        return self.date_sent.strftime('%d/%m/%Y %H:%M:%S')

    def __str__(self) -> str:
        return f"Notificação: {self.message} - {self.get_formatted_date_sent()} - {self.receiver_id}"
    
    def to_json(self) -> dict[str, Any]:
        """Converte os dados do Objeto para JSON."""
        return {
            "notif_id": self.id,
            "message": self.message,
            "date_sent": self.get_formatted_date_sent(),
            "receiver_id": self.receiver_id,
            "receiver_type": self.receiver_type.value
        }

    @staticmethod
    def from_json(data: dict[str, Any]) -> "Notification":
        """Ler dados JSON e converte para um Objeto dessa Classe."""
        return Notification(data["notif_id"], data["message"], datetime.strptime(data["date_sent"], "%d/%m/%Y %H:%M:%S"), data["receiver_id"], UsersTypeIDs(data["receiver_type"]))

class NotificationDAO(AbstractDAO):
    _objects: list[Notification] = []
    _json_file_path_str: str = "../data/notifications.json"
    _from_json_method = Notification.from_json
