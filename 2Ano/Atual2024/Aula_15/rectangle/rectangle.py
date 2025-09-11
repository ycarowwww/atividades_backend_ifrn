from math import sqrt

class Rectangle:
    def __init__(self, base: float, height: float) -> None:
        self.__base = base
        self.__height = height
    
    def calc_area(self) -> float: return self.__base * self.__height

    def calc_diagonal(self) -> float: return sqrt(self.__base ** 2 + self.__height ** 2)

    def __str__(self) -> str:
        return f"Rectangle: {self.__base} base and {self.__height} height"
    