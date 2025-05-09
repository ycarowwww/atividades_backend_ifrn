print(1 - 2 + 3 * 4)  # 11
print(1 * 2 - 3 * 4)  # -10
print(1 / 2 + 3 * 4)  # 12.5
print(1 // 2 * 3 + 4) # 4
print(1 + 2 * 3 / 4)  # 2.5

print(sum([ int(i) for i in input("Numbers: ").split() if int(i) % 2 == 0 ]))

print("".join([ l for i, l in enumerate(list(input("Phrase: "))) if i % 2 == 0 ]))

class WaterBill:
    def __init__(self, month: int, year: int, consumption: float) -> None:
        self.__month = month
        self.__year = year
        self.__consumption = consumption

    def get_value(self) -> float:
        if self.__consumption <= 10: return 38
        elif self.__consumption <= 20: return 38 + 5 * (self.__consumption - 10)
        return 38 + 5 * 20 + 6 * (self.__consumption - 20)

month = int(input("Month: "))
year = int(input("Year: "))
consumption = float(input("Consumption: "))
bill = WaterBill(month, year, consumption)
print(bill.get_value())
