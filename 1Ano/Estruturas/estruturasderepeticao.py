print(" 1 - Saída 1 \n 2 - Saída 2 \n 3 - Saída 3 \n 4 - Números Inteiros de 1 a 30 \n 5 - Números Inteiros entre [-5; 5] \n 6 - Números Pares entre [2; 10] \n 7 - Múltiplos de 3 entre [1; 20] \n 8 - Programa FizzBuzz \n 9 - Inteiro Positivo N de 1 - N \n 10 - Inteiros entre -N e N \n 11 - Múltiplos de 3 entre 1 e N \n 12 - Programa FizzBuzz 2 \n 13 - Saída 4 \n 14 - Inteiros de [1; n] \n 15 - Inteiros de [-n; n] \n 16 - Pares entre [2; n] \n 17 - Quantidade de Vogais em uma String \n 18 - Inteiro n e Pirâmide de Números \n 19 - Inteiro n e Pirâmide de Números Inversa")
question: str = input()

print("-" * 50)

match question:
    case "1":
        # Saída: 1 \ 2 \ 3 \ Fim
        x = 1
        while x < 4:
            print(x)
            x = x + 1
        print("Fim")
    case "2":
        # Saída: 1 \ 3 \ 5 \ 7 \ Fim
        x = 1
        while x <= 7:
            print(x)
            x = x + 2
        print("Fim")
    case "3":
        # Saída: 1 \ 1 \ 1 \ ...
        x = 1
        while x <= 5:
            print(x)
        print("Fim")
    case "4":
        print(" - ".join(str(i) for i in range(1, 31)))
    case "5":
        print(" - ".join(str(i) for i in range(-5, 6)))
    case "6":
        print(" - ".join(str(i) for i in range(1, 11) if i % 2 == 0))
    case "7":
        print(" - ".join(str(i) for i in range(1, 20) if i % 3 == 0))
    case "8":
        numbers: list[int] = [i for i in range(1, 20+1)]
        for i in numbers:
            if i % 3 == 0 and i % 5 == 0:
                print("FizzBuzz", end=" - ")
            elif i % 3 == 0:
                print("Fizz", end=" - ")
            elif i % 5 == 0:
                print("Buzz", end=" - ")
            else:
                print(i, end=" - ")
        print("Fim!")
    case "9":
        print(" - ".join(str(i) for i in range(int(input())+1)))
    case "10":
        number: int = int(input())
        print(" - ".join(str(i) for i in range(-number, number+1)))
    case "11":
        print(" - ".join(str(i) for i in range(1, int(input())+1) if i % 3 == 0))
    case "12":
        numbers: list[int] = [i for i in range(1, int(input())+1)]
        for i in numbers:
            if i % 3 == 0 and i % 4 == 0:
                print("FizzBuzz", end=" - ")
            elif i % 3 == 0:
                print("Fizz", end=" - ")
            elif i % 4 == 0:
                print("Buzz", end=" - ")
            else:
                print(i, end=" - ")
        print("Fim!")
    case "13":
        # 0, 1, 2, 3
        print("\033[33m a) \033[m")
        for i in range(4):
            print(i)
        print("\033[33m b) \033[m")
        # 0, 3, 6, 9, 12, 15
        for i in range(0, 17, 3):
            print(i)
    case "14":
        print("\n".join(str(i) for i in range(1, int(input())+1)))
    case "15":
        number: int = int(input())
        print("\n".join(str(i) for i in range(-number, number+1)))
    case "16":
        print("\n".join(str(i) for i in range(2, int(input())+1, 2)))
    case "17":
        print(sum(1 for i in input().lower() if i in {'a', 'e', 'i', 'o', 'u'}))
    case "18":
        for i in range(1, int(input())+1):
            print(*range(1, i+1))
    case "19":
        for i in range(int(input()), 0, -1):
            print(*range(1, i+1))
    case _:
        print("Opção Inválida/Inexistente!")