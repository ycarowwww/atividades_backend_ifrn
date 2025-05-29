class Freight:
    def __init__(self, distance: float, weight: float) -> None:
        self.distance = distance
        self.weight = weight
    
    @property
    def distance(self) -> float: return self.__distance

    @distance.setter
    def distance(self, new_distance: float) -> None:
        if not isinstance(new_distance, (int, float)): raise TypeError("Distance must be a number.")
        if new_distance <= 0: raise ValueError("Distance must be greater than 0.")
        self.__distance = new_distance
    
    @property
    def weight(self) -> float: return self.__weight

    @weight.setter
    def weight(self, new_weight: float) -> None:
        if not isinstance(new_weight, (int, float)): raise TypeError("Weight must be a number.")
        if new_weight <= 0: raise ValueError("Weight must be greater than 0.")
        self.__weight = new_weight
    
    def price(self) -> float:
        return self.distance * self.weight * 0.01
    
    def __str__(self) -> str:
        return f"A Freight with distance {self.distance} km and weight {self.weight} kg."
