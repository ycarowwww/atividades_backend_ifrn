class Country:
    def __init__(self, country_id: int, name: str, population: int, area: float) -> None:
        self.country_id = country_id
        self.name = name
        self.population = population
        self.area = area
    
    @property
    def country_id(self) -> int: return self.__country_id
    
    @country_id.setter
    def country_id(self, new_country_id: int) -> None:
        if not isinstance(new_country_id, int): raise TypeError("Country ID needs to be an int.") # type: ignore
        
        self.__country_id = new_country_id
    
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
        if not isinstance(new_population, int): raise TypeError("Population needs to be an int.") # type: ignore
        if new_population <= 0: raise ValueError("Population can't be negative.")
        
        self.__population = new_population

    @property
    def area(self) -> float: return self.__area
    
    @area.setter
    def area(self, new_area: float) -> None:
        if not isinstance(new_area, (int, float)): raise TypeError("Area needs to be a number.") # type: ignore
        if new_area <= 0: raise ValueError("Area can't be negative.")
        
        self.__area = new_area

    def population_density(self) -> float: return self.population / self.area

    def __str__(self) -> str: return f"{self.country_id} - País {self.name} com {self.population} habitantes e {self.area} km²."

class CountryList:
    def __init__(self) -> None:
        self.__current_index: int = 0
        self.__list_countries: dict[int, Country] = {}
    
    @property
    def list_countries(self) -> list[Country]: return [ i for i in self.__list_countries.values() ]
    
    def append(self, new_name: str, new_population: int, new_area: float) -> None:
        new_country = Country(self.__current_index, new_name, new_population, new_area)
        self.__list_countries[self.__current_index] = new_country
        self.__current_index += 1
    
    def update(self, index: int, new_name: str, new_population: int, new_area: float) -> None:
        if index not in self.__list_countries: raise IndexError("Index inexistent.")

        country = self.__list_countries[index]
        country.name = new_name
        country.population = new_population
        country.area = new_area

    def remove(self, index: int) -> None:
        if index not in self.__list_countries: raise IndexError("Index inexistent.")

        self.__list_countries.pop(index)
    
    def more_populous(self) -> list[Country]:
        if len(self.__list_countries) <= 0: return []

        max_pop = 0
        countries: list[Country] = []

        for c in self.list_countries:
            if c.population == max_pop:
                countries.append(c)
            elif c.population > max_pop:
                max_pop = c.population
                countries.clear()
                countries.append(c)
                
        return countries

    def more_populated(self) -> list[Country]:
        if len(self.__list_countries) <= 0: return []

        max_density = 0
        countries: list[Country] = []

        for c in self.list_countries:
            if c.population_density() == max_density:
                countries.append(c)
            elif c.population_density() > max_density:
                max_density = c.population_density()
                countries.clear()
                countries.append(c)
                
        return countries

class CountryUI:
    __countries = CountryList()

    @classmethod
    def main(cls) -> None:
        while True:
            option = cls.menu()

            match option:
                case 1: cls.append_country()
                case 2: cls.list_countries()
                case 3: cls.update_country()
                case 4: cls.remove_country()
                case 5: cls.show_more_populous()
                case 6: cls.show_more_populated()
                case 7:
                    print("Saindo do Programa...")
                    break
                case _:
                    print("Opção Inválida!")
    
    @staticmethod
    def menu() -> int:
        print("=" * 50)
        print(f"{'Menu':^50}")
        print("=" * 50)
        print("1 - Inserir um novo país no cadastro\n2 - Listar todos os países\n3 - Atualizar os dados de um país\n4 - Excluir um país do cadastro\n5 - Mostrar o país mais populoso\n6 - Mostrar o país mais povoado\n7 - Sair")
        return int(input("- Selecione uma opção acima: "))

    @classmethod
    def append_country(cls) -> None:
        print("=" * 50)
        print(f"{'Novo País':^50}")
        print("=" * 50)

        new_name = input("- Nome do país: ")
        new_population = int(input("- População do país: "))
        new_area = float(input("- Área do país: "))
        cls.__countries.append(new_name, new_population, new_area)
        print("País Inserido com Sucesso!")

    @classmethod
    def list_countries(cls) -> None:
        print("=" * 50)
        print(f"{'Listar Países':^50}")
        print("=" * 50)

        countries = cls.__countries.list_countries
        for c in countries:
            print(c)

    @classmethod
    def update_country(cls) -> None:
        print("=" * 50)
        print(f"{'Atualizar País':^50}")
        print("=" * 50)

        index = int(input("- Index do País: "))
        new_name = input("- Novo nome do País: ")
        new_population = int(input("- Nova população do País: "))
        new_area = float(input("- Nova área do País: "))
        cls.__countries.update(index, new_name, new_population, new_area)
        print("País Atualizado com Sucesso!")

    @classmethod
    def remove_country(cls) -> None:
        print("=" * 50)
        print(f"{'Remover País':^50}")
        print("=" * 50)

        index = int(input("- Index do País: "))
        cls.__countries.remove(index)
        print("País Removido com Sucesso!")

    @classmethod
    def show_more_populous(cls) -> None:
        print("=" * 50)
        print(f"{'Países mais Populosos':^50}")
        print("=" * 50)

        countries = cls.__countries.more_populous()
        if len(countries) <= 0: print("Não há países na lista.")
        else:
            for c in countries:
                print(f"{c.country_id} - {c.name} : {c.population} habitantes")

    @classmethod
    def show_more_populated(cls) -> None:
        print("=" * 50)
        print(f"{'Países mais Povoados':^50}")
        print("=" * 50)

        countries = cls.__countries.more_populated()
        if len(countries) <= 0: print("Não há países na lista.")
        else: 
            for c in countries:
                print(f"{c.country_id} - {c.name} : {c.population_density()} h/km²")

if __name__ == '__main__':
    CountryUI.main()
