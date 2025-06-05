class Trip:
    def __init__(self, destination: str, distance: float, liters: float) -> None:
        self.destination = destination
        self.distance = distance
        self.liters = liters
    
    @property
    def destination(self) -> str: return self.__destination

    @destination.setter
    def destination(self, new_destination: str) -> None:
        new_destination = new_destination.strip()
        if new_destination == "": raise ValueError("Destination can't be empty.")

        self.__destination = new_destination
    
    @property
    def distance(self) -> float: return self.__distance

    @distance.setter
    def distance(self, new_distance: float) -> None:
        if not isinstance(new_distance, (int, float)): raise TypeError("Distance needs to be a number.")
        if new_distance <= 0: raise ValueError("Distance needs to be greater than 0.")
        
        self.__distance = new_distance
    
    @property
    def liters(self) -> float: return self.__liters

    @liters.setter
    def liters(self, new_liters: float) -> None:
        if not isinstance(new_liters, (int, float)): raise TypeError("Liters needs to be a number.")
        if new_liters <= 0: raise ValueError("The amount of liters consumed needs to be greater than 0.")

        self.__liters = new_liters

    def consumption(self) -> float:
        return self.distance / self.liters

    def __str__(self) -> str:
        return f"Uma Viagem para {self.destination} a {self.distance} km de distância em que {self.liters} litros serão consumidos."

class TripUI:
    @staticmethod
    def menu() -> int:
        print(f"{'Menu':^50}")
        print("=" * 50)
        print("1 - Calcular\n2 - Fim")
        option: int = int(input("Opção Selecionada: "))
        return option
    
    @staticmethod
    def main() -> None:
        while True:
            option: int = TripUI.menu()

            match option:
                case 1:
                    TripUI.calculate()
                case 2:
                    print("Saindo do Programa...")
                    return
                case _:
                    print("Opção Inválida!")
    
    @staticmethod
    def calculate() -> None:
        print(f"{'Insira os dados da Viagem':^50}")
        print("-"*50)

        destination: str = input("Destino da Viagem: ")
        distance: float = float(input("Distância [km]: "))
        liters: float = float(input("Combustível necessário [litros]: "))

        trip: Trip = Trip(destination, distance, liters)

        print(trip)

        print(f"Consumo Médio: {trip.consumption()} km/l")
    
if __name__ == "__main__":
    TripUI.main()
