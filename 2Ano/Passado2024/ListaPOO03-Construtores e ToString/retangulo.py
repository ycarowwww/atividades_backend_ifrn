from math import hypot

class Rectangle:
    def __init__(self, base: float, height: float) -> None:
        self.__base = base
        self.__height = height
    
    def set_base(self, new_base: float) -> None:
        if new_base > 0:
            self.__base = new_base
            return
        raise ValueError("Base cannot be less than or equal to 0!")
    
    def set_height(self, new_height: float) -> None:
        if new_height > 0:
            self.__height = new_height
            return
        raise ValueError("Height cannot be less than or equal to 0!")

    def get_base(self) -> float: return self.__base

    def get_height(self) -> float: return self.__height

    def calc_area(self) -> float: return self.__base * self.__height

    def calc_diagonal(self) -> float: return hypot(self.__base, self.__height)

    def __str__(self) -> str: return f"Base: {self.__base} | Height: {self.__height}"