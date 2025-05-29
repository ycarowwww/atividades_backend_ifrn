from math import sqrt

class Rectangle:
    def __init__(self, base: float, height: float) -> None:
        self.base = base
        self.height = height
    
    @property
    def base(self) -> float: return self.__base

    @base.setter
    def base(self, new_base: float) -> None:
        if not isinstance(new_base, (int, float)): raise TypeError("Base must be a number.")
        if new_base <= 0: raise ValueError("Base must be greater than 0.")
        self.__base = new_base
    
    @property
    def height(self) -> float: return self.__height

    @height.setter
    def height(self, new_height: float) -> None:
        if not isinstance(new_height, (int, float)): raise TypeError("Height must be a number.")
        if new_height <= 0: raise ValueError("Height must be greater than 0.")
        self.__height = new_height
    
    def area(self) -> float:
        return self.base * self.height
    
    def diagonal(self) -> float:
        return sqrt(self.base ** 2 + self.height ** 2)
    
    def __str__(self) -> str:
        return f"A Rectangle with base {self.base} and height {self.height}"
