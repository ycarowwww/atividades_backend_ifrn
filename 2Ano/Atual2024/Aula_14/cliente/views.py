from models import Client, ClientDAO

class View:
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
