class Country:
    def __init__(self, country_id: int, name: str, population: int, area: float) -> None:
        self.__country_id = country_id
        self.__name = name
        self.__population = population
        self.__area = area

    @property
    def country_id(self) -> int: return self.__country_id

    @property
    def name(self) -> str: return self.__name

    @property
    def population(self) -> int: return self.__population

    @property
    def area(self) -> float: return self.__area

    def density(self) -> float: return self.population / self.area

    def __str__(self) -> str:
        return f"{self.country_id} - {self.name} : {self.population} habitantes e {self.area} km²"
