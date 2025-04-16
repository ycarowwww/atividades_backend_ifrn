print("Lista 04 de POO")
print("-" * 50)
print("1 - Formula de Bhaskara\n2 - Múltiplos\n3 - Animal\n4 - DDD\n5 - Tira-teima\n6 - Máquina de Café\n7 - Números Pares\n8 - Maior e Posição\n9 - Experiências\n10 - Senha Fixa\n11 -  Dividindo X por Y\n12 - Fibonacci Fácil")
option: str = input("Selecione uma Opção acima: ")

print("-" * 50)
match option:
    case "1":
        a, b, c = map(float, input().split())
        d = b ** 2 - 4 * a * c

        if d < 0 or a == 0:
            print("Impossivel calcular")
        else:
            r1 = (-b + d ** 0.5) / (2 * a)
            r2 = (-b - d ** 0.5) / (2 * a)
            print(f"R1 = {r1:.5f}")
            print(f"R2 = {r2:.5f}")
    case "2":
        a, b = map(int, input().split())
        print("Sao Multiplos" if a % b == 0 or b % a == 0 else "Nao sao Multiplos")
    case "3":
        p1, p2, p3 = [ input() for _ in range(3) ]
        words = {
            "vertebrado": {
                "ave" : {
                    "carnivoro" : "aguia",
                    "onivoro" : "pomba"
                },
                "mamifero" : {
                    "herbivoro" : "vaca",
                    "onivoro" : "homem"
                }
            },
            "invertebrado": {
                "inseto" : {
                    "hematofago" : "pulga",
                    "herbivoro" : "lagarta"
                },
                "anelideo" : {
                    "hematofago" : "sanguessuga",
                    "onivoro" : "minhoca"
                }
            }
        }
        print(words[p1][p2][p3])
    case "4":
        num = input()
        ddds = {
            "61" : "Brasilia",
            "71" : "Salvador",
            "11" : "Sao Paulo",
            "21" : "Rio de Janeiro",
            "32" : "Juiz de Fora",
            "19" : "Campinas",
            "27" : "Vitoria",
            "31" : "Belo Horizonte"
        }
        if ddds.get(num) == None:
            print("DDD nao cadastrado")
        else:
            print(ddds.get(num))
    case "5":
        n1, n2 = map(int, input().split())

        if 0 <= n1 <= 432 and 0 <= n2 <= 468:
            print("dentro")
        else:
            print("fora")
    case "6":
        a1, a2, a3 = [ int(input()) for _ in range(3) ]

        print(min(
            a2 * 2 + a3 * 4, 
            a1 * 2 + a3 * 2, 
            a1 * 4 + a2 * 2
        ))
    case "7":
        for i in range(2, 101, 2):
            print(i)
    case "8":
        largest, ind = int(input()), 1
        for i in range(2, 101):
            new_num = int(input())
            if new_num > largest:
                largest = new_num
                ind = i
        print(largest)
        print(ind)
    case "9":
        amount = int(input())
        total, rabbits, rats, frogs = 0, 0, 0, 0

        for _ in range(amount):
            test_amount, test_type = input().split()
            test_amount = int(test_amount)
            total += test_amount

            if test_type == "C":
                rabbits += test_amount
            elif test_type == "R":
                rats += test_amount
            else:
                frogs += test_amount
        
        print(f"Total: {total} cobaias")
        print(f"Total de coelhos: {rabbits}")
        print(f"Total de ratos: {rats}")
        print(f"Total de sapos: {frogs}")
        print(f"Percentual de coelhos: {rabbits / total * 100:.2f} %")
        print(f"Percentual de ratos: {rats / total * 100:.2f} %")
        print(f"Percentual de sapos: {frogs / total * 100:.2f} %")
    case "10":
        while True:
            password = input()
            if password != "2002":
                print("Senha Invalida")
            else:
                print("Acesso Permitido")
                break
    case "11":
        amount = int(input())
        answers = []

        for _ in range(amount):
            a, b = map(int, input().split())
            if b == 0:
                answers.append("divisao impossivel")
            else:
                answers.append(a / b)
        
        print(*answers, sep="\n")
    case "12":
        amount = int(input())
        fibonacci_numbers = [0, 1, 1]
        if amount < 3:
            fibonacci_numbers = fibonacci_numbers[:amount]
        else:
            for _ in range(amount-3):
                fibonacci_numbers.append(fibonacci_numbers[-2] + fibonacci_numbers[-1])
        print(*fibonacci_numbers, sep=" ")
    case _:
        print("Opção Inválida!")
