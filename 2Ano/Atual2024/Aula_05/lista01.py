from math import pi

print("Lista 01 de POO")
print("-" * 50)
print("1 - Um Círculo\n2 - Uma Viagem\n3 - Uma Conta Bancária\n4 - Uma Entrada de Cinema")
option: str = input("Selecione uma Opção acima: ")

class Circle:
    def __init__(self, radius: float) -> None:
        self.__radius = radius
    
    def get_area(self) -> float: return pi * self.__radius ** 2

    def get_circumference(self) -> float: return 2 * pi * self.__radius

class Trip:
    def __init__(self, distance: float, hours: float, minutes: float) -> None:
        self.__distance = distance
        self.__time = hours + minutes / 60
    
    def get_average_speed(self) -> float: return self.__distance / self.__time

class BankAccount:
    def __init__(self, name: str, number: int) -> None:
        self.__name = name
        self.__number = number
        self.__balance = 0.0
    
    def deposit(self, amount: float) -> None:
        self.__balance += amount
    
    def withdraw(self, amount: float) -> None:
        self.__balance -= amount
    
    def get_balance(self) -> float: return self.__balance

class MovieSession:
    def __init__(self, day: str, hour: int) -> None:
        self.__day = day
        self.__hour = hour
        self.__is_always_half = False
        self.__base_entrance = self.calculate_entrance()
    
    def calculate_entrance(self) -> float:
        v = 16
        
        if self.__day in ["segunda", "terça", "quinta"]:
            v = 16
        elif self.__day == "quarta":
            v = 8.0
            self.__is_always_half = True
            return v
        elif self.__day in ["sexta", "sábado", "domingo"]:
            v = 20.0
        
        if self.__hour == 0 or self.__hour >= 17:
            v *= 1.5
        
        return v
    
    def get_entrance(self) -> float:
        return self.__base_entrance
    
    def get_half_entrance(self) -> float:
        if self.__is_always_half: return self.__base_entrance
        return self.__base_entrance / 2

print("-" * 50)
match option:
    case "1":
        radius = float(input("Insira o raio do Círculo: "))
        circle = Circle(radius)
        
        print(f"Área: {circle.get_area()}")
        print(f"Circunferência: {circle.get_circumference()}")
    case "2":
        distance = float(input("Insira a distância da viagem em km: "))
        time = list(map(int, input("Insira o tempo da viagem em [hh:mm]: ").split(":")))
        trip = Trip(distance, time[0], time[1])
        
        print(f"Velocidade Média: {trip.get_average_speed()}")
    case "3":
        name = input("Insira seu Nome: ")
        number = int(input("Insira seu Número: "))
        account = BankAccount(name, number)

        account.deposit(10.0)
        account.withdraw(3.0)
        print(account.get_balance())
        account.withdraw(13.0)
        print(account.get_balance())
        account.deposit(20.0)
        print(account.get_balance())
    case "4":
        session = MovieSession("sábado", 14)

        print(session.get_entrance())
        print(session.get_half_entrance())
    case _:
        print("Opção Inválida!")
