from datetime import datetime, timedelta
from typing import Any, Type, Optional
from models import *

class View:
    # Métodos Abstratos - Todos os DAOs tem um "padrão", esses métodos recebem o DAO e chamam o método apropriado.
    @staticmethod
    def get_all(dao_class: Type[AbstractDAO]) -> list[Any]: return dao_class.get_all()

    @staticmethod
    def get_id(dao_class: Type[AbstractDAO], obj_id: int) -> Optional[Any]: return dao_class.get_id(obj_id)
    
    @staticmethod
    def add(dao_class: Type[AbstractDAO], obj: Any) -> None:
        dao_class.add(obj)
    
    @staticmethod
    def update(dao_class: Type[AbstractDAO], obj: Any) -> None:
        dao_class.update(obj)
    
    @staticmethod
    def delete(dao_class: Type[AbstractDAO], obj: Any) -> None:
        dao_class.delete(obj)
    
    # Métodos - Cliente.
    @staticmethod
    def get_client_list() -> list[Client]:
        items: list[Client] = View.get_all(ClientDAO)
        items.sort(key=lambda i: i.id)
        return items

    @staticmethod
    def get_client(client_id: int) -> Optional[Client]: return View.get_id(ClientDAO, client_id)

    @staticmethod
    def append_client(name: str, email: str, phone: str, password: str) -> None:
        View.add(ClientDAO, Client(0, name, email, phone, password))
    
    @staticmethod
    def update_client(client_id: int, name: str, email: str, phone: str, password: str) -> None:
        View.update(ClientDAO, Client(client_id, name, email, phone, password))
    
    @staticmethod
    def remove_client(client_id: int) -> None:
        View.delete(ClientDAO, Client(client_id, "_", "_", "_", "_"))
    
    # Métodos - Serviço.
    @staticmethod
    def get_service_list() -> list[Service]: 
        items: list[Service] = View.get_all(ServiceDAO)
        items.sort(key=lambda i: i.id)
        return items

    @staticmethod
    def get_service(service_id: int) -> Optional[Service]: return View.get_id(ServiceDAO, service_id)

    @staticmethod
    def append_service(description: str, value: float) -> None:
        View.add(ServiceDAO, Service(0, description, value))

    @staticmethod
    def update_service(service_id: int, description: str, value: float) -> None:
        View.update(ServiceDAO, Service(service_id, description, value))

    @staticmethod
    def remove_service(service_id: int) -> None:
        View.delete(ServiceDAO, Service(service_id, "_", 0))
    
    # Métodos - Horário.
    @staticmethod
    def get_schedule_list() -> list[Schedule]: 
        items: list[Schedule] = View.get_all(ScheduleDAO)
        items.sort(key=lambda i: i.date)
        return items

    @staticmethod
    def get_schedule(schedule_id: int) -> Optional[Schedule]: return View.get_id(ScheduleDAO, schedule_id)

    @staticmethod
    def append_schedule(date: datetime, confirmed: bool, client: Optional[Client], service: Optional[Service], professional: Optional[Professional]) -> None:
        client_id = client.id if isinstance(client, Client) else 0
        service_id = service.id if isinstance(service, Service) else 0
        professional_id = professional.id if isinstance(professional, Professional) else 0
        View.add(ScheduleDAO, Schedule(0, date, confirmed, client_id, service_id, professional_id))

    @staticmethod
    def update_schedule(schedule_id: int, date: datetime, confirmed: bool, client: Optional[Client], service: Optional[Service], professional: Optional[Professional]) -> None:
        client_id = client.id if isinstance(client, Client) else 0
        service_id = service.id if isinstance(service, Service) else 0
        professional_id = professional.id if isinstance(professional, Professional) else 0
        View.update(ScheduleDAO, Schedule(schedule_id, date, confirmed, client_id, service_id, professional_id))

    @staticmethod
    def remove_schedule(schedule_id: int) -> None:
        View.delete(ScheduleDAO, Schedule(schedule_id, datetime(1900, 1, 2)))
    
    @staticmethod
    def append_multiple_schedules(date_beginning: datetime, date_ending: datetime, interval_minutes: int, professional: Professional) -> None:
        while date_beginning <= date_ending:
            View.append_schedule(date_beginning, False, None, None, professional)
            date_beginning += timedelta(minutes=interval_minutes)
    
    # Métodos - Profissional.
    @staticmethod
    def get_professional_list() -> list[Professional]: 
        items: list[Professional] = View.get_all(ProfessionalDAO)
        items.sort(key=lambda i: i.id)
        return items

    @staticmethod
    def get_professional(prof_id: int) -> Optional[Professional]: return View.get_id(ProfessionalDAO, prof_id)

    @staticmethod
    def append_professional(name: str, email: str, speciality: str, council: str, password: str) -> None:
        View.add(ProfessionalDAO, Professional(0, name, email, speciality, council, password))

    @staticmethod
    def update_professional(prof_id: int, name: str, email: str, speciality: str, council: str, password: str) -> None:
        View.update(ProfessionalDAO, Professional(prof_id, name, email, speciality, council, password))

    @staticmethod
    def remove_professional(prof_id: int) -> None:
        View.delete(ProfessionalDAO, Professional(prof_id, "_", "_", "_", "_", "_"))

    # Métodos - Admin.
    @staticmethod
    def get_admin_list() -> list[Admin]: 
        items: list[Admin] = View.get_all(AdminDAO)
        items.sort(key=lambda i: i.id)
        return items

    @staticmethod
    def get_admin(admin_id: int) -> Optional[Admin]: return View.get_id(AdminDAO, admin_id)

    @staticmethod
    def append_admin(name: str, email: str, password: str) -> None:
        View.add(AdminDAO, Admin(0, name, email, password))
    
    @staticmethod
    def update_admin(admin_id: int, name: str, email: str, password: str) -> None:
        View.update(AdminDAO, Admin(admin_id, name, email, password))
    
    @staticmethod
    def remove_admin(admin_id: int) -> None:
        View.delete(AdminDAO, Admin(admin_id, "_", "_", "_"))

    # Filtração.
    @staticmethod
    def get_schedules_to_setting(prof_id: int) -> list[Schedule]:
        """Retorna os horários permitidos para serem agendados."""
        schedules: list[Schedule] = []
        today_time = datetime.now()
        
        for schedule in View.get_schedule_list():
            if (schedule.professional_id == prof_id
                    and schedule.date >= today_time
                    and schedule.client_id == 0
                    and schedule.confirmed == False):
                schedules.append(schedule)

        return schedules

    @staticmethod
    def get_schedules_by_client(client_id: int) -> list[Schedule]:
        """Retornar os Horários de um Cliente específico."""
        wanted_schedules: list[Schedule] = []
        schedules = View.get_schedule_list()

        for schedule in schedules:
            if schedule.client_id == client_id:
                wanted_schedules.append(schedule)

        return wanted_schedules

    @staticmethod
    def get_schedules_by_professional(prof_id: int) -> list[Schedule]:
        """Retornar os Horários de um Profissional específico."""
        wanted_schedules: list[Schedule] = []
        schedules = View.get_schedule_list()

        for schedule in schedules:
            if schedule.professional_id == prof_id:
                wanted_schedules.append(schedule)

        return wanted_schedules

    # Autenticação.
    @staticmethod
    def auth_user(email: str, password: str) -> Optional[tuple[int, int]]:
        """Retorna o ID e Tipo do Usuário."""
        clients = View.get_client_list()
        professionals = View.get_professional_list()
        admins = View.get_admin_list()
        users_type = View.get_users_type()
        
        for client in clients:
            if client.email == email and client.password == password:
                return (client.id, users_type.CLIENT)
        
        for prof in professionals:
            if prof.email == email and prof.password == password:
                return (prof.id, users_type.PROFESSIONAL)

        for admin in admins:
            if admin.email == email and admin.password == password:
                return (admin.id, users_type.ADMIN)
        
    @staticmethod
    def get_users_type() -> Type[UsersTypeIDs]:
        """Retorna os tipos de Usuários (Enum)."""
        return UsersTypeIDs
