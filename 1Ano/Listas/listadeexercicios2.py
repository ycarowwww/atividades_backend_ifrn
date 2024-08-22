from math import prod, sqrt

print(" 1 - Soma dos Inteiros [1; 10] \n 2 - Soma dos Inteiros de [1; n] \n 3 - Soma dos Pares dos Inteiros de [1; n] \n 4 - Produtório dos Inteiros de [1; n] \n 5 - Produtório dos Números Ímpares de [1; n] \n 6 - Soma dos Pares e Ímpares de [1; n] \n 7 - Soma dos Inteiros entre [a; b] \n 8 - Quantidade de Números \n 9 - Soma de Números fornecidos \n 10 - Raiz Quadrada de n \n 11 - Descrecência de n até 1 \n 12 - Divisores de n \n 13 - MDC(a, b) \n 14 - MMC(a, b) \n 15 - Soma dos Inteiros de [1; n] \n 16 - Soma dos Ímpares e Pares de [1; n] \n 17 - Tabuada de n \n 18 - '*' n vezes \n 19 - '*' n vezes na direita \n 20 - '*' n vezes no centro \n 21 - Soma de 1 até n")
question: str = input("- Escolha uma das Questões: ")

match question:
    case '1':
        print(sum(range(11)))
    case '2':
        print(sum(range(int(input())+1)))
    case '3':
        print(sum(i for i in range(int(input())+1) if i % 2 == 0))
    case '4':
        print(prod(range(1, int(input())+1)))
    case '5':
        print(prod(i for i in range(int(input())+1) if i % 2 != 0))
    case '6':
        number: int = int(input())
        print(f"Soma dos Pares: {sum(i for i in range(number+1) if i % 2 == 0)}")
        print(f"Soma dos Ímpares: {sum(i for i in range(number+1) if i % 2 != 0)}")
    case '7':
        n1, n2 = [int(input()) for _ in range(2)]
        sign: int = int(abs(n2 - n1) / (n2 - n1)) if n1 != n2 else 1
        print(sum(range(n1, n2+sign, sign)))
    case '8':
        numbers: list[int] = []
        while True:
            n: int = int(input())
            if n == 0: break
            numbers.append(n)
        print(len(numbers))
    case '9':
        numbers: list[int] = []
        while True:
            n: int = int(input())
            if n == 0: break
            numbers.append(n)
        print(sum(numbers))
    case '10':
        number: float = float(input())
        print(f"{sqrt(number):.2f}" if number >= 0 else "Informe um valor não-negativo.")
    case '11':
        print(" ".join(str(i) for i in range(int(input()), 0, -1)))
    case '12':
        number: int = int(input())
        print(" ".join(str(i) for i in range(number, 0, -1) if number % i == 0))
    case '13':
        numbers: list[int] = [int(input()) for _ in range(2)]
        while numbers[1] != 0: 
            numbers = [numbers[1], numbers[0] % numbers[1]]
        print(numbers[0])
    case '14':
        numbers: list[int] = [int(input()) for _ in range(2)]
        amount, b = numbers
        while b != 0:
            amount, b = b, amount % b
        print(abs(numbers[0] * numbers[1]) // amount)
    case '15':
        number: int = int(input())
        if number <= 1:
            print("Informe um valor maior do que 1")
        else:
            print(" + ".join(str(i) for i in range(1, number+1)), end=" = ")
            print(sum(range(1, number+1)))
    case '16':
        number: int = int(input())
        if number > 3:
            print(f"Números Ímpares: {" + ".join(str(i) for i in range(1, number+1) if i % 2 != 0)}", end=" = ")
            print(sum(i for i in range(1, number+1) if i % 2 != 0))
            print(f"Números Pares: {" + ".join(str(i) for i in range(1, number+1) if i % 2 == 0)}", end=" = ")
            print(sum(i for i in range(1, number+1) if i % 2 == 0))
        else:
            print("Informe um valor maior do que 3")
    case '17':
        number: int = int(input())

        for i in range(0, 11):
            print(f"{number} x {i} = {number*i}")
    case '18':
        for i in range(1, int(input())+1):
            print("*" * i)
    case '19':
        amount: int = int(input())
        for i in range(1, amount+1):
            print(f"{"*"*i:>{amount}}")
    case '20':
        amount: int = int(input())*2
        for i in range(1, amount, 2):
            print(f"{"*"*i:^{amount}}")
    case '21':
        number: int = int(input())
        if number > 2:
            print(f"{" + ".join(str(i) for i in range(1, number+1))} = {sum(range(1, number+1))}")
        else:
            print("Informe um valor maior que 2.")
    case _:
        print("Selecione uma questão válida!")