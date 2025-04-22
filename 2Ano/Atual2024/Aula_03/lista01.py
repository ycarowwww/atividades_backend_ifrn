print("Lista 01 de POO")
print("-" * 50)
print("1 - Maior Número\n2 - Média Aritmética\n3 - Soma de Par e Ímpar\n4 - Soma de Horas\n5 - Identificador de Mês\n6 - Soma do menor com o maior\n7 - Equação Quadrática\n8 - 4 Valores Diferentes\n9 - Ângulos dos ponteiros") # It's incomplete
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
    case _:
        print("Opção Inválida!")
