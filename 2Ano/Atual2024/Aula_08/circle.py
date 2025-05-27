from math import pi

class Circle:
    """
    Circle class with radius property and some methods for circle's formulas.

    Attributes:
        radius (float): Radius of the circle (must be positive).
    """
    
    def __init__(self, radius: float) -> None:
        """
        Initialize a Circle instance.

        Args:
            radius (float): Radius of the circle (must be positive).
        
        Raises:
            ValueError: If radius is not positive.
        """
        self.radius = radius
    
    @property
    def radius(self) -> float:
        """Circle's Radius."""
        return self.__radius
    
    @radius.setter
    def radius(self, new_radius: float) -> None:
        if isinstance(new_radius, (int, float)) and new_radius > 0:
            self.__radius = new_radius
        else:
            raise ValueError("Radius must be a number and greater than 0.")
    
    def area(self) -> float:
        """Return the area of the circle."""
        return pi * self.radius ** 2
    
    def circumference(self) -> float:
        """Return the circumference of the circle."""
        return 2 * pi * self.radius

if __name__ == "__main__":
    radius: float = float(input("- Enter the Circle's radius: "))
    
    c1: Circle = Circle(radius)

    print(f"Area: {c1.area()}")
    print(f"Circumference: {c1.circumference()}")
