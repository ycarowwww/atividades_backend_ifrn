import math

def ConvertToBool(text: str):
    if (text == "TRUE"):
        return True
    else:
        return False

print(" 1 - Output 1 \n 2 - Output 2 \n 3 - Output 3 \n 4 - Output 4 \n 5 - Output 5 \n 6 - Valor da Comissão \n 7 - Preço do Sorvete \n 8 - Preço de Caixas de Frutas \n 9 - Ordenar Números \n 10 - ~ \n 11 - Calcular Raiz Quadrada Real \n 12 - Horas, Minutos e Segundos \n 13 - ~ \n 14 - Categorias de Nadadores \n 15 - Conversor de Meses \n 16 - IMC")
choice = input("\033[0;34mEscolha uma das Opções acima: \033[m\033[1;36m")

print("\033[0;37m=\033[m" * 75)

if (choice == "1"): # Output 1
    print("\033[33ma = 5\nb = 3\nc = 2\nprint(a > 1)\nprint(b < 9)\nprint(c >= a)\nprint(b <= 3)\nprint(a >= a)\nprint(a == b)\nprint(b == 2)\nprint(c != c)\nprint(c != a)\033[m")
    print("\033[30m=\033[m" * 75)
    a = 5
    b = 3
    c = 2
    print(a > 1)
    print(b < 9)
    print(c >= a)
    print(b <= 3)
    print(a >= a)
    print(a == b)
    print(b == 2)
    print(c != c)
    print(c != a)
elif (choice == "2"): # Output 2
    print("a = True\nb = False\nprint(a and b)\nprint(a and a)\nprint(b and b)\nprint(b and a)")
    print("\033[30m=\033[m" * 75)
    a = True
    b = False
    print(a and b)
    print(a and a)
    print(b and b)
    print(b and a)
elif (choice == "3"): # Output 3
    print("a = True\nb = False\nprint(a or b)\nprint(a or a)\nprint(b or b)\nprint(b or a)")
    print("\033[30m=\033[m" * 75)
    a = True
    b = False
    print(a or b)
    print(a or a)
    print(b or b)
    print(b or a)
elif (choice == "4"): # Output 4
    print("a = True\nb = False\nprint(a)\nprint(not a)\nprint(b)\nprint(not b)")
    print("\033[30m=\033[m" * 75)
    a = True
    b = False
    print(a)
    print(not a)
    print(b)
    print(not b)
elif (choice == "5"): # Output 5
    print("A = 2\nB = 7\nC = False\nB == A * 2\nB > A + 5\nB > A or B == A\nC and B / A == 3.5\nnot C and C\nB >= 0 and B < 5\nA < 0 or A >= 1\nA % 2 != 0\nTrue or C and A + 1 < B\n(True or C) and A + 1 < B")
    print("\033[30m=\033[m" * 75)
    A = 2
    B = 7
    C = False
    print(B == A * 2)
    print(B > A + 5)
    print(B > A or B == A)
    print(C and B / A == 3.5)
    print(not C and C)
    print(B >= 0 and B < 5)
    print(A < 0 or A >= 1)
    print(A % 2 != 0)
    print(True or C and A + 1 < B)
    print((True or C) and A + 1 < B)
elif (choice == "6"): # Valor da Comissão
    value = float(input("\033[0;32mDigite um valor: \033[m\033[1;36m"))
    commission_percentage = float(input("\033[0;35mDigite a porcentagem da comissão: \033[m\033[1;36m")) / 100

    commission = commission_percentage * value
    if (value > 5000):
        commission += 300

    print(f"\033[0;31mComissão: \033[m\033[1;33m{commission:.2f}\033[m")
elif (choice == "7"): # Preço do Sorvete
    print("\033[0;32m - Valor do Sorvete: \033[m\033[1;36mR$4.00\033[m \n \033[0;33m- Valor da Cobertura: \033[m\033[1;36mR$1.50\033[m \n \033[0;34m- Valor do Granulado: \033[m\033[1;36mR$1.00\033[m \n \033[0;35m- Valor dos Canudos de Biscoito: \033[m\033[1;36mR$0.5 /c\033[m")
    ice_cream = 4.00
    additions = 0.00

    print("\033[0;37m-\033[m" * 50)

    topping = ConvertToBool((input("\033[0;33mVocê gostaria de \033[m\033[1;35mCobertura\033[m\033[0;33m? \033[0;30m[True/False]\033[m\033[0;33m:\033[m \033[1;36m")).upper())
    if topping == True:
        additions += 1.50

    sprinkles = ConvertToBool((input("\033[0;33mVocê gostaria de \033[m\033[1;35mGranulado\033[m\033[0;33m? \033[0;30m[True/False]\033[m\033[0;33m:\033[m \033[1;36m")).upper())
    if sprinkles == True:
        additions += 1.00

    straws = ConvertToBool((input("\033[0;33mVocê gostaria de \033[m\033[1;35mCanudos de Biscoito\033[m\033[0;33m? \033[0;30m[True/False]\033[m\033[0;33m:\033[m \033[1;36m")).upper())
    if straws == True:
        additions += 0.5 * float(input("\033[0;30m-\033[m\033[0;35m Quantos\033[m\033[0;34m Canudos?: \033[m\033[1;36m"))
    
    final_price = ice_cream + additions
    
    print(f"\033[0;34mO\033[m\033[1;31m Preço Total\033[m\033[0;34m será de: \033[m\033[1;32m{final_price:.2f}\033[m")
elif (choice == "8"): # Preço de Caixas de Frutas
    amount_box = int(input("\033[0;33mDigite a \033[1;32mquantidade de Caixas\033[m\033[0;33m a serem compradas: \033[m\033[1;36m"))
    box = 30.00

    if (amount_box >= 5):
        discount = 2.00 * amount_box
    else:
        discount = 0.00
    
    final_price = amount_box * box - discount

    print(f"\033[0;34mO \033[m\033[1;35mPreço Final\033[m\033[0;34m das Caixas será de: \033[m\033[0;31m{final_price:.2f}\033[m")
elif (choice == "9"): # Ordenar Números
    n = int(input("\033[0;35mDigite a \033[m\033[1;32mQuantidade de Números\033[m\033[0;35m a serem digitados: \033[m\033[1;36m"))

    numbers = [float(input(f"\033[0;33mDigite o Número {_ + 1}: \033[m\033[1;36m")) for _ in range(n)]

    print("\033[0;37m-\033[m" * 50)
    print(" \033[1;31mFalse\033[m\033[0;33m - Crescente\033[m \n \033[1;32mTrue\033[m\033[0;33m  - Decrescente\033[m")
    numbers.sort(reverse = (ConvertToBool((input("\033[0;34m- Escolha uma das opções para organizar essa lista: \033[m\033[1;36m")).upper())))

    print(f"\033[0;30mLista Organizada: \033[m\033[1;36m{numbers}\033[m")
elif (choice == "11"): # Calcular Raiz Quadrada Real
    n = float(input("\033[0;30mDigite um Número: \033[m\033[1;36m"))

    if (n >= 0):
        print(f"\033[0;33mA Raiz Quadrada de \033[m\033[1;32m{n}\033[m\033[0;33m é: \033[m\033[1;36m{(n**(1/2)):.4f}\033[m")
    else:
        print("\033[0;33mPara \033[m\033[1;31mNúmeros Negativos\033[m\033[0;33m, não há raízes \033[m\033[1;35mreais\033[m")
elif (choice == "12"): # Horas, Minutos e Segundos
    print(" \033[1;33m1\033[m\033[30m - Segundos\033[m \n \033[1;34m2\033[m\033[30m - Minutos\033[m \n \033[1;35m3\033[m\033[30m - Horas\033[m")
    option = input("\033[33mEscolha uma Opção para a Transfomação: \033[m\033[1;36m")

    time = float(input("\033[33m- Digite a \033[m\033[1;32mQuantidade\033[m\033[33m de Tempo: \033[m\033[1;36m"))

    if (option == "1"):
        hours = time // 3600
        minutes = (time % 3600) // 60
        seconds = (time % 3600) % 60
    elif (option == "2"):
        hours = time // 60
        minutes = math.trunc(time % 60)
        seconds = ((time % 60) - math.trunc(time % 60)) * 60
    elif (option == "3"):
        hours = math.trunc(time)
        minutes = (time - math.trunc(time)) * 60
        seconds = (((time - math.trunc(time)) * 60) - math.trunc((time - math.trunc(time)) * 60)) * 60
    else:
        print("\033[1;31mOpção Inválida!\033[m")
        hours = 0
        minutes = 0
        seconds = 0

    print(f" \033[1;33mHoras: \033[m\033[1;36m{hours:.0f}\033[m \n \033[1;36mMinutos: \033[m\033[1;32m{minutes:.0f}\033[m \n \033[1;35mSegundos: \033[m\033[1;36m{seconds:.0f}\033[m")
elif (choice == "14"): # Categorias de Nadadores
    age = int(input("\033[33m- Digite a \033[m\033[1;32mIdade\033[m\033[33m do Nadador: \033[m\033[1;36m"))

    if (5 <= age <= 7):
        category = "Peixinho"
    elif (8 <= age <= 10):
        category = "Infantil A"
    elif (11 <= age <= 13):
        category = "Infantil B"
    elif (14 <= age <= 17):
        category = "Juvenil"
    elif (age >= 18):
        category = "Adulto"
    else:
        category = "Inválida / Inexistente"
    
    print(f"\033[0;35mA Categoria do Nadador é: \033[m\033[1;36m{category}\033[m")
elif (choice == "15"): # Conversor de Meses
    month = {
        1 : "Janeiro",
        2 : "Fevereiro",
        3 : "Março",
        4 : "Abril",
        5 : "Maio",
        6 : "Junho",
        7 : "Julho",
        8 : "Agosto",
        9 : "Setembro",
        10 : "Outubro",
        11 : "Novembro",
        12 : "Dezembro"
    }

    n = int(input("\033[33m- Digite o \033[m\033[1;32mNúmero\033[m\033[33m de um \033[m\033[1;35mMês\033[m\033[33m: \033[m\033[1;36m"))
    
    print(f"\033[0;30mO \033[m\033[1;32mMês \033[m\033[1;35m{n}\033[m\033[30m é: \033[m\033[1;36m{month.get(n, "Inexistente")}\033[m")
elif (choice == "16"): # IMC
    weight = float(input("\033[0;30m- Digite seu \033[m\033[1;35mPeso\033[m\033[0;30m: \033[m\033[1;36m"))
    height = float(input("\033[0;30m- Digite sua \033[m\033[1;35mAltura\033[m\033[0;30m: \033[m\033[1;36m"))
    imc = weight / height ** 2

    if (imc < 18.5):
        category = "Baixo Peso"
    elif (imc < 24.9):
        category = "Peso Normal"
    elif (imc < 29.9):
        category = "Sobrepeso"
    elif (imc < 39.9):
        category = "Obesidade"
    else:
        category = "Obesidade Grave"
    
    print(f"\033[0;32m IMC: \033[m\033[1;36m{imc:.2f}\033[m \n \033[0;32mCategoria: \033[m\033[1;36m{category}\033[m")
else:
    print("\033[4;31mOpção Inválida!\033[m")