class Triangle:
    def __init__(self, base: float, height: float) -> None:
        self.__base = base
        self.__height = height
    
    def calc_area(self) -> float:
        return self.__base * self.__height / 2
    
class UI:
    @staticmethod
    def read_inputs() -> tuple[float, float]:
        base: float = float(input("- Enter the Triangle's Base: "))
        height: float = float(input("- Enter the Triangle's Height: "))
        return (base, height)

    @staticmethod
    def menu() -> str:
        print("1 - Calculate Triangle's Area\n2 - Leave the Program")
        print("-" * 50)
        option: str = input("- Select an option above: ")
        return option
    
    @staticmethod
    def main() -> None:
        while True:
            option: str = UI.menu()

            match option:
                case "1":
                    base, height = UI.read_inputs()
                    triangle: Triangle = Triangle(base, height)
                    print(f"Area: {triangle.calc_area()}")
                case "2":
                    print("Leaving Program...")
                    break
                case _:
                    print("Invalid Option!")
            
            print("-" * 50)

UI.main()
