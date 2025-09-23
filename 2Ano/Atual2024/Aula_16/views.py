from datetime import datetime
from models.client import Client, ClientDAO
from models.service import Service, ServiceDAO
from models.schedule import Schedule, ScheduleDAO

class View:
    # Client methods.
    @staticmethod
    def get_client_list() -> list[Client]: return ClientDAO.get_clients()

    @staticmethod
    def get_client(client_id: int) -> Client | None: return ClientDAO.get_client(client_id)

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
    def get_service(service_id: int) -> Service | None: return ServiceDAO.get_service(service_id)

    @staticmethod
    def append_service(description: str, value: float) -> None:
        ServiceDAO.append(Service(0, description, value))

    @staticmethod
    def update_service(service_id: int, description: str, value: float) -> None:
        ServiceDAO.update(Service(service_id, description, value))

    @staticmethod
    def remove_service(service_id: int) -> None:
        ServiceDAO.remove(Service(service_id, "_", 0))
    
    # Schedule methods.
    @staticmethod
    def get_schedule_list() -> list[Schedule]: return ScheduleDAO.get_schedules()

    @staticmethod
    def get_schedule(schedule_id: int) -> Schedule | None: return ScheduleDAO.get_schedule(schedule_id)

    @staticmethod
    def append_schedule(date: datetime, confirmed: bool, client: Client | None, service: Service | None) -> None:
        client_id = client.id if isinstance(client, Client) else 0
        service_id = service.id if isinstance(service, Service) else 0
        ScheduleDAO.append(Schedule(0, date, confirmed, client_id, service_id))

    @staticmethod
    def update_schedule(schedule_id: int, date: datetime, confirmed: bool, client: Client | None, service: Service | None) -> None:
        client_id = client.id if isinstance(client, Client) else 0
        service_id = service.id if isinstance(service, Service) else 0
        ScheduleDAO.update(Schedule(schedule_id, date, confirmed, client_id, service_id))

    @staticmethod
    def remove_schedule(schedule_id: int) -> None:
        ScheduleDAO.remove(Schedule(schedule_id, datetime(1900, 1, 2)))
