from cmath import sqrt

class QuadraticEquation:
    def __init__(self, a: float, b: float, c: float) -> None:
        self.a = a
        self.b = b
        self.c = c
    
    @property
    def a(self) -> float: return self.__a

    @a.setter
    def a(self, new_a: float) -> None:
        if not isinstance(new_a, (int, float)): raise TypeError("A must be a number.")
        if new_a == 0: raise ValueError("A must not be 0.")
        self.__a = new_a
    
    @property
    def b(self) -> float: return self.__b

    @b.setter
    def b(self, new_b: float) -> None:
        if not isinstance(new_b, (int, float)): raise TypeError("B must be a number.")
        self.__b = new_b
    
    @property
    def c(self) -> float: return self.__c

    @c.setter
    def c(self, new_c: float) -> None:
        if not isinstance(new_c, (int, float)): raise TypeError("C must be a number.")
        self.__c = new_c

    def delta(self) -> float: return self.b ** 2 - 4 * self.a * self.c

    def have_real_roots(self) -> bool: return self.delta() >= 0

    def root1(self) -> float: return (-self.b + sqrt(self.delta())) / (2 * self.a)

    def root2(self) -> float: return (-self.b - sqrt(self.delta())) / (2 * self.a)

    def __str__(self) -> str:
        return f"A Quadratic Equation with a = {self.a}, b = {self.b} and c = {self.c}"
