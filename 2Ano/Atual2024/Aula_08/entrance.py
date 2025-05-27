class CinemaEntrance:
    def __init__(self, day: str, hour: int) -> None:
        self.day = day
        self.hour = hour
    
    @property
    def day(self) -> str:
        return self.__day
    
    @day.setter
    def day(self, new_day: str) -> None:
        self.__day = new_day
    
    @property
    def hour(self) -> int:
        return self.__hour
    
    @hour.setter
    def hour(self, new_hour: int) -> None:
        self.__hour = new_hour
    
    def get_entrance(self) -> float:
        if self.day == "wednesday": return 8.0
        
        value: float = 0
        if self.day in [ "monday", "tednesday", "thursday" ]: value = 16.0
        else: value = 20.0
        
        if 17 <= self.hour < 24: value *= 1.5

        return value

    def get_half_entrance(self) -> float:
        if self.day == "wednesday": return 8.0

        return self.get_entrance() / 2
