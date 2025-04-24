print("Lista 01 de POO")
print("-" * 50)
print("1 - Maior Número\n2 - Média Aritmética\n3 - Soma de Par e Ímpar\n4 - Soma de Horas\n5 - Identificador de Mês\n6 - Soma do menor com o maior\n7 - Equação Quadrática\n8 - 4 Valores Diferentes\n9 - Ângulos dos ponteiros\n10 - Verificador de Datas\n11 - Leitor de Datas\n12 - Operações com inteiros\n13 - Maior e Menor valores\n14 - Analisador de Triângulo\n15 - Organizador de Valores")
option: str = input("Selecione uma Opção acima: ")

print("-" * 50)
match option:
    case "1":
        n1 = int(input())
        n2 = int(input())
        if n1 == n2:
            print("Número iguais")
        else:
            print(f"Maior = {max(n1, n2)}")
    case "2":
        print("Digite 4 números inteiros:")
        nums = [ int(input()) for _ in range(4) ]
        mean = sum(nums) / len(nums)
        
        print(f"Média = {mean}")
        print(f"Números menores que a média: {' '.join([ str(n) for n in nums if n < mean ])}")
        print(f"Números maiores ou iguais a média: {' '.join([ str(n) for n in nums if n >= mean ])}")
    case "3":
        print("Digite 4 números inteiros:")
        nums = [ int(input()) for _ in range(4) ]

        print(f"Soma dos pares = {sum([n for n in nums if n % 2 == 0])}")
        print(f"Soma dos ímpares = {sum([n for n in nums if n % 2 != 0])}")
    case "4":
        hour1 = input("Primeiro Horário no formato hh:mm: ").split(":")
        hour2 = input("Primeiro Horário no formato hh:mm: ").split(":")

        minutes = (int(hour1[1]) + int(hour2[1]))
        hours = (int(hour1[0]) + int(hour2[0])) + minutes // 60
        minutes %= 60

        print(f"{hours:02d}:{minutes:02d}")
    case "5":
        months = {
            "1" : "janeiro",
            "2" : "fevereiro",
            "3" : "março",
            "4" : "abril",
            "5" : "maio",
            "6" : "junho",
            "7" : "julho",
            "8" : "agosto",
            "9" : "setembro",
            "10" : "outubro",
            "11" : "novembro",
            "12" : "dezembro"
        }
        month_num = input("Número do Mês: ")

        print(f"O mês de {months[month_num]} está no {(int(month_num)-1) // 3 + 1}º trimestre do ano")
    case "6":
        print("Digite 3 números inteiros:")
        nums = [ int(input()) for _ in range(3) ]

        print(f"Soma do maior e do menor: {min(nums) + max(nums)}")
    case "7":
        a = float(input("Coeficiente A: "))
        b = float(input("Coeficiente B: "))
        c = float(input("Coeficiente C: "))

        delta = b ** 2 - 4 * a * c
        if delta < 0:
            print("Impossível Calcular")
        else:
            r1 = (-b + delta ** (1/2)) / (2 * a)
            r2 = (-b - delta ** (1/2)) / (2 * a)

            print(f"As raízes são {r1} e {r2}")
    case "8":
        print("Digite 4 números inteiros:")
        nums = [ int(input()) for _ in range(4) ]

        if len(set(nums)) != 4:
            print("Os Valores devem ser diferentes...")
        else:
            nums.sort()
            
            print(f"Maior valor = {nums[3]}")
            print(f"Menor valor = {nums[0]}")
            print(f"Soma dos 2º = {nums[1] + nums[2]}")
    case "9":
        time = [int(i) for i in input("Digite um horário no formato hh:mm: ").split(":")]

        if 0 <= time[0] < 24 and 0 <= time[1] < 60:
            angle_minute = 360 / 60 * time[1]
            angle_hour = 360 / 12 * time[0] + 360 / 12 * (time[1] / 60)
            smaller_angle_between = min(abs(angle_hour - angle_minute), 360 - abs(angle_hour - angle_minute))
            print(f"Menor Ângulo entre os ponteiros: {smaller_angle_between}")
        else:
            print("Hora Inválida")
    case "10":
        day, month, year = [ int(i) for i in input("Digite uma data no formato dd/mm/aaaa: ").split("/") ]
        is_leap_year = True if year % 400 == 0 else (True if year % 4 == 0 and year % 100 != 0 else False)
        days_per_month: dict[int, int] = {
            1 : 31,
            2 : 28 + (1 if is_leap_year else 0),
            3 : 31,
            4 : 30,
            5 : 31,
            6 : 30,
            7 : 31,
            8 : 31,
            9 : 30,
            10 : 31,
            11 : 30,
            12 : 31
        }

        if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= days_per_month[month]:
            print("Data Válida")
        else:
            print("Data Inválida")
    case "11":
        day, month, year = [ int(i) for i in input("Digite uma data no formato dd/mm/aaaa: ").split("/") ]
        months = {
            1 : "janeiro",
            2 : "fevereiro",
            3 : "março",
            4 : "abril",
            5 : "maio",
            6 : "junho",
            7 : "julho",
            8 : "agosto",
            9 : "setembro",
            10 : "outubro",
            11 : "novembro",
            12 : "dezembro"
        }

        print(f"A data é {day} de {months[month]} de {year}")
    case "12":
        expression = input("Digite dois valores inteiros separados por um operador +, -, * ou /: ")

        operation = None
        for char in expression:
            if char in "+-*/":
                operation = char
                break

        numbers = [ int(i) for i in expression.split(operation) ]
        
        print("Resultado: ", end="")
        match operation:
            case "+":
                print(numbers[0] + numbers[1])
            case "-":
                print(numbers[0] - numbers[1])
            case "*":
                print(numbers[0] * numbers[1])
            case "/":
                print(numbers[0] / numbers[1])
            case _:
                print("Operação Inválida")
    case "13":
        nums = input("Digite dez valores inteiros:\n").split()

        print(f"O maior é {max(nums)} e o menor é {min(nums)}")
    case "14":
        print("Digite os lados do triângulo:")
        sides = [ int(input()) for _ in range(3) ]

        if sides[0] + sides[1] > sides[2] and sides[0] + sides[2] > sides[1] and sides[2] + sides[1] > sides[0]:
            print("Triângulo válido!")

            if sides[0] == sides[1] == sides[2]:
                print("Triângulo Equilátero")
            elif sides[0] == sides[1] or sides[0] == sides[2] or sides[1] == sides[2]:
                print("Triângulo Isósceles")
            else:
                print("Triângulo Escaleno")
        else:
            print("Triângulo inválido!")
    case "15":
        print("Digite 3 valores:")
        nums = [ int(input()) for _ in range(3) ]
        nums.sort()
        print(", ".join([ str(n) for n in nums ]))
    case _:
        print("Opção Inválida!")
