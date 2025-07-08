from datetime import datetime

class Paciente:
    def __init__(self, nome: str, cpf: str, telefone: str, nascimento: datetime) -> None:
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.nascimento = nascimento

    @property
    def nome(self) -> str: return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        nome = nome.strip()
        if nome == "": raise ValueError("Name can't be empty.")
        self.__nome = nome

    @property
    def cpf(self) -> str: return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str) -> None:
        cpf = cpf.strip()
        if cpf == "": raise ValueError("CPF can't be empty.")
        self.__cpf = cpf

    @property
    def telefone(self) -> str: return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str) -> None:
        telefone = telefone.strip()
        if telefone == "": raise ValueError("Phone number can't be empty.")
        self.__telefone = telefone

    @property
    def nascimento(self) -> datetime: return self.__nascimento

    @nascimento.setter
    def nascimento(self, nascimento: datetime) -> None:
        if nascimento.year <= 1900: raise ValueError("Invalid Date.")
        self.__nascimento = nascimento

    def idade(self) -> str:
        current_date = datetime.today()
        difference_dates = current_date - self.nascimento
        years = difference_dates.days // 365
        months = difference_dates.days % 365 // 30
        return f"{years} anos e {months} meses"

    def __str__(self) -> str:
        return f"Paciente {self.nome} - {self.cpf} - {self.telefone} - {self.nascimento}"

class PacienteUI:
    @staticmethod
    def menu() -> str:
        print("1 - Novo Paciente\n2 - Sair")
        return input("- Selecione uma opção acima: ")
    
    @staticmethod
    def main() -> None:
        while True:
            option = PacienteUI.menu()

            match option:
                case "1": PacienteUI.analyse_patient()
                case "2": 
                    print("Saindo do programa")
                    break
                case _: print("Opção Inválida!")

    @staticmethod
    def analyse_patient() -> None:
        nome = input("- Insira nome do Paciente: ")
        cpf = input("- Insira CPF do Paciente: ")
        telefone = input("- Insira telefone do Paciente: ")
        nascimento = [ int(i) for i in  input("- Insira data de nascimento do Paciente [DD/MM/YYYY]: ").split("/") ]
        nascimento = datetime(nascimento[2], nascimento[1], nascimento[0])
        paciente = Paciente(nome, cpf, telefone, nascimento)
        print(f"Idade do Paciente: {paciente.idade()}")
        print(paciente)

if __name__ == "__main__":
    PacienteUI.main()
