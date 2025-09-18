from models.client import Client, ClientDAO
from models.service import Service, ServiceDAO

class View:
    # Client methods.
    @staticmethod
    def get_client_list() -> list[Client]: return ClientDAO.get_clients()

    @staticmethod
    def append_client(name: str, email: str, phone: str) -> None:
        ClientDAO.append(Client(0, name, email, phone))
    
    @staticmethod
    def update_client(client_id: int, name: str, email: str, phone: str) -> None:
        ClientDAO.update(Client(client_id, name, email, phone))
    
    @staticmethod
    def remove_client(client_id: int) -> None:
        ClientDAO.remove(Client(client_id, "_", "_", "_"))
    
    # Service methods.
    @staticmethod
    def get_service_list() -> list[Service]: return ServiceDAO.get_services()

    @staticmethod
    def append_service(description: str, value: float) -> None:
        ServiceDAO.append(Service(0, description, value))

    @staticmethod
    def update_service(service_id: int, description: str, value: float) -> None:
        ServiceDAO.update(Service(service_id, description, value))

    @staticmethod
    def remove_service(service_id: int) -> None:
        ServiceDAO.remove(Service(service_id, "_", 0))
