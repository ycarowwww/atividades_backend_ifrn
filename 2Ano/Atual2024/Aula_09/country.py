class Country:
    def __init__(self, name: str, population: int, area: float) -> None:
        self.name = name
        self.population = population
        self.area = area

    @property
    def name(self) -> str: return self.__name

    @name.setter
    def name(self, new_name: str) -> None:
        new_name = new_name.strip()
        if new_name == "": raise ValueError("Name can't be empty.")

        self.__name = new_name

    @property
    def population(self) -> int: return self.__population

    @population.setter
    def population(self, new_population: int) -> None:
        if not isinstance(new_population, int): raise TypeError("Population needs to be an integer.")
        if new_population < 0: raise ValueError("Population needs greater than or equal to 0.")

        self.__population = new_population

    @property
    def area(self) -> float: return self.__area

    @area.setter
    def area(self, new_area: float) -> None:
        if not isinstance(new_area, (int, float)): raise TypeError("Area needs to be a number.")
        if new_area < 0: raise ValueError("Area needs greater than or equal to 0.")

        self.__area = new_area

    def density(self) -> float:
        return self.population / self.area
    
    def __str__(self) -> str:
        return f"O país {self.name} possui {self.population} habitantes com {self.area} km² de área."

class CountryUI:
    @staticmethod
    def menu() -> int:
        print(f"{'Menu':^50}")
        print("=" * 50)
        print("1 - Calcular\n2 - Fim")
        option: int = int(input("Opção Selecionada: "))
        return option

    @staticmethod
    def main() -> None:
        while True:
            option: int = CountryUI.menu()

            match option:
                case 1:
                    CountryUI.calculate()
                case 2:
                    print("Saindo do Programa...")
                    return
                case _:
                    print("Opção Inválida!")
    
    @staticmethod
    def calculate() -> None:
        print(f"{'Insira os dados do País':^50}")
        print("-"*50)

        name: str = input("Nome do País: ")
        population: int = int(input("População do País: "))
        area: float = float(input("Área do País [km²]: "))

        country: Country = Country(name, population, area)

        print(country)

        print(f"Densidade Demográfica: {country.density()}")

CountryUI.main()
