from datetime import date

class Patient:
    def __init__(self, name: str, cpf: str, phone: str, birthday: date) -> None:
        self.__name = name
        self.__cpf = cpf
        self.__phone = phone
        self.__birthday = birthday
    
    def age(self) -> str:
        age = (date.today() - self.__birthday).days
        years = age // 365
        months = (age - 365 * years) // 30

        return [years, months]
    
    def __str__(self) -> str:
        birthday = f"{self.__birthday.year} {self.__birthday.month} {self.__birthday.day}"
        return f"Patient: {self.__name} {self.__cpf} {self.__phone} {birthday}"
