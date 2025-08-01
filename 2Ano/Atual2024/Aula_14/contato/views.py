from models import Contact, ContactDAO
from datetime import datetime

class View:
    @staticmethod
    def append_contact(name: str, email: str, number: str, birthday: str) -> None:
        birthday_datetime = datetime.strptime(birthday, "%d/%m/%Y")
        new_contact = Contact(0, name, email, number, birthday_datetime)
        ContactDAO.append(new_contact)
    
    @staticmethod
    def get_contact_list() -> list[Contact]: return ContactDAO.get_contacts()

    @staticmethod
    def get_contact(contact_id: int) -> Contact | None: return ContactDAO.get_contact(contact_id)

    @staticmethod
    def update_contact(contact_id: int, name: str, email: str, number: str, birthday: str) -> None:
        birthday_datetime = datetime.strptime(birthday, "%d/%m/%Y")
        updated_contact = Contact(contact_id, name, email, number, birthday_datetime)
        ContactDAO.update_contact(updated_contact)
    
    @staticmethod
    def remove_contact(contact_id: int) -> None:
        ContactDAO.remove(Contact(contact_id, "_", "_@_", "_", datetime(2000, 1, 1)))
    
    @staticmethod
    def search_by_initial(initial: str) -> list[Contact]: 
        return ContactDAO.search_by_initial(initial.lower())

    @staticmethod
    def search_birthmonth(month: int) -> list[Contact]:
        if month < 1 or month > 12: return []
        return ContactDAO.search_by_birthmonth(month)
