class Trip:
    def __init__(self, distance: float, time: float) -> None:
        self.distance = distance
        self.time = time
    
    @property
    def distance(self) -> float:
        return self.__distance
    
    @distance.setter
    def distance(self, new_distance: float) -> None:
        if isinstance(new_distance, (int, float)):
            self.__distance = new_distance
        else:
            raise ValueError("Distance must be a number.")
    
    @property
    def time(self) -> float:
        return self.__time
    
    @time.setter
    def time(self, new_time: float) -> None:
        if isinstance(new_time, (int, float)) and new_time:
            self.__time = new_time
        else:
            raise ValueError("Time must be a number.")
    
    def mean_speed(self) -> float:
        return self.distance / self.time

if __name__ == "__main__":
    distance: float = float(input("- Enter the Trip's distance [km]: "))
    time: float = float(input("- Enter the Trip's time [h]: "))
    
    c1: Trip = Trip(distance, time)

    print(f"Mean Speed: {c1.mean_speed()} km/h")
