class BankAccount:
    def __init__(self, name: str, number: str, initial_balance: float) -> None:
        self.name = name
        self.number = number
        self.__balance = initial_balance
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, new_name: str) -> None:
        self.__name = new_name
    
    @property
    def number(self) -> str:
        return self.__number
    
    @number.setter
    def number(self, new_number: str) -> None:
        self.__number = new_number
    
    @property
    def balance(self) -> float:
        return self.__balance
    
    def deposit(self, amount: float) -> None:
        self.__balance += amount
    
    def withdraw(self, amount: float) -> None:
        self.__balance -= amount

if __name__ == "__main__":
    name: str = input("Name: ")
    number: str = input("Number: ")
    initial_balance: float = float(input("Initial Balance: "))

    account1: BankAccount = BankAccount(name, number, initial_balance)

    print(account1.name)
    print(account1.number)
    print(account1.balance)

    account1.deposit(5)
    print(account1.balance)
    account1.withdraw(8)
    print(account1.balance)
