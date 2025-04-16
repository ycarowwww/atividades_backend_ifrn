print("Lista 03 de POO")
print("-" * 50)
print("1 - Produto Simples\n2 - Média 1\n3 - Esfera\n4 - Corrida\n5 - Distância Entre Dois Pontos\n6 - Tomadas")
option: str = input("Selecione uma Opção acima: ")

print("-" * 50)
match option:
    case "1":
        a = int(input())
        b = int(input())
        PROD = a * b
        print(f"PROD = {PROD}")
    case "2":
        a = float(input()) * 3.5
        b = float(input()) * 7.5
        print(f"MEDIA = {(a + b) / 11:.5f}")
    case "3":
        r = int(input())
        print(f"VOLUME = {4 / 3 * 3.14159 * r ** 3:.3f}")
    case "4":
        a, b = [int(i) for i in input().split()]
        print(a % b)
    case "5":
        x1, y1 = [float(i) for i in input().split()]
        x2, y2 = [float(i) for i in input().split()]
        print(f"{((x2-x1) ** 2 + (y2-y1) ** 2) ** 0.5:.4f}")
    case "6":
        nums = [int(i) for i in input().split()]

        if max(nums) >= 3:
            print(sum(nums) - 3)
        else:
            print(5)
    case _:
        print("Opção Inválida!")
