from math import trunc, ceil

def main():
    print(" 1  - Nome na Caixa \n 2  - Somar Números \n 3  - Somar Áreas de Quadrados \n 4  - Média de Números \n 5  - Multiplicação com 1 casa decimal \n 6  - Nome com Asteriscos \n 7  - ~ \n 8  - Dobro de um Número \n 9  - ~ \n 10  - ~ \n 11  - ~ \n 12  - Menor de n Números \n 13 - Operações Matemáticas \n 14 - Média só com o Meio \n 15 - Horas \n 16 - Área Dividida por 1,5")
    choice = input("\033[33m- Escolha uma das Opções: \033[m\033[1;36m")

    print("\033[1;30m=\033[m" * 50)

    if (choice == "1"): # Nome na Caixa
        name = input("\033[35mDigite seu nome: \033[m\033[1;32m")
        l = "+" + "-" * (len(name) + 2) + "+"

        print(f"\033[30m {l} \n | {name} | \n {l}\033[m")
    elif (choice == "2"): # Somar Números
        limit = int(input("\033[35mDigite a quantidade de Números: \033[m\033[1;36m"))

        numbers = []

        for i in range(limit):
            numbers.append(float(input(f"\033[34mDigite o Número \033[m\033[1;30m{i+1}\033[m\033[34m: \033[m\033[1;32m")))

        print(f"\033[33mA \033[m\033[1;35mSoma\033[m\033[33m desses \033[m\033[1;35m{len(numbers)}\033[m\033[33m números dá: \033[m\033[1;36m{sum(numbers)}\033[m")
    elif (choice == "3"): # Somar Áreas de Quadrados
        q1 = float(input("\033[34mLado do \033[m\033[1;32mQuadrado 1\033[m\033[34m: \033[m\033[1;36m"))
        q2 = float(input("\033[34mLado do \033[m\033[1;32mQuadrado 2\033[m\033[34m: \033[m\033[1;36m"))

        res = (q1**2) + (q2**2)

        print(f"\033[33mA \033[m\033[1;35mSoma\033[m\033[33m desses Quadrados é: \033[m\033[1;36m{res}\033[m")
    elif (choice == "4"): # Média de Números
        limit = int(input("\033[34mDigite a \033[m\033[1;32mQuantidade\033[m\033[34m de Números: \033[m\033[1;36m"))

        numbers = []

        for i in range(limit):
            numbers.append(float(input("\033[30mDigite um Número: \033[m\033[1;35m")))

        media = sum(numbers) / len(numbers)

        print(f"\033[33mA \033[m\033[31mMédia\033[m\033[33m desses \033[m\033[31m{len(numbers)}\033[m\033[33m Números aproximada é: \033[m\033[1;36m{media:.1f}\033[m")
    elif (choice == "5"): # Multiplicação com 1 casa decimal
        num = float(input("\033[34mDigite um Número: \033[m\033[1;36m"))
        num2 = float(input("\033[34mDigite um Outro Número: \033[m\033[1;36m"))
        res = num * num2

        print(f"\033[33mA \033[m\033[1;35mMultiplicação\033[m\033[33m de \033[1;32m{num}\033[m\033[33m e \033[m\033[1;32m{num2}\033[m\033[33m dá: \033[m\033[1;36m{res:.1f}\033[m")
    elif (choice == "6"): # Nome com Asteriscos
        name = input("\033[30mDigite o seu Nome: \033[m\033[1;36m")

        qasterisk = int(input("\033[30mDigite a Quantidade de Asteriscos: \033[m\033[1;36m"))
        asterisk = "*" * qasterisk

        print(f"\033[32m{asterisk} {name} {asterisk}\033[m")
    elif (choice == "8"): # Dobro de um Número
        num = int(input("\033[33mDigite um Número: \033[m\033[1;36m"))
        dnum = num * 2

        print(f"\033[30mO \033[m\033[1;32mDobro\033[m\033[30m de \033[1;35m{num}\033[m\033[30m é: \033[m\033[1;36m{dnum}\033[m")
    elif (choice == "12"): # Menor de n Números
        limit = int(input("\033[33mDigite a \033[m\033[1;32mQuantidade\033[m\033[33m de \033[m\033[35mNúmeros\033[m\033[33m: \033[m\033[1;36m"))

        numbers = []
        
        for i in range(limit):
            numbers.append(float(input(f"\033[30mDigite o Número \033[m\033[1;35m{i+1}\033[m\033[33m: \033[m\033[1;36m")))

        print(f"\033[30mO \033[m\033[1;35mMenor\033[m\033[30m Número desses Números é o: \033[m\033[1;31m{min(numbers)}\033[m")
    elif (choice == "13"): # Operações Matemáticas
        num = int(input("\033[30mDigite um \033[m\033[1;33mNúmero Inteiro Positivo\033[m\033[30m: \033[m\033[1;36m"))

        if (num <= 0):
            print(f"\033[33mO Número \033[m\033[32m{num}\033[m\033[33m é \033[m\033[1;31mmenor ou igual\033[m\033[33m a \033[m\033[1;35mZero\033[m\033[33m!\033[m")
        else:
            print(f"\033[30m- O \033[m\033[35mQuadrado\033[m\033[30m de \033[m\033[32m{num}\033[m\033[30m é: \033[m\033[1;36m{num**2}\033[m")
            print(f"\033[30m- A \033[m\033[35mRaiz Quadrada\033[m\033[30m de \033[m\033[32m{num}\033[m\033[30m é: \033[m\033[1;36m{num**(1/2):.2f}\033[m")
            print(f"\033[30m- A \033[m\033[35mRaiz Cúbica\033[m\033[30m de \033[m\033[32m{num}\033[m\033[30m é: \033[m\033[1;36m{num**(1/3):.2f}\033[m")
    elif (choice == "14"): # Média só com o Meio
        limit = int(input("\033[30mDigite a \033[m\033[1;32mQuantidade\033[m\033[30m de Números: \033[m\033[1;36m"))

        if (limit < 3):
            print(f"\033[34mA Quantidade de números têm que ser de pelo menos \033[m\033[31m3 números!\033[m")
            limit = 3
        
        numbers = []

        for i in range(limit):
            numbers.append(float(input("\033[30mDigite um Número: \033[m\033[1;36m")))
        
        numbers.remove(min(numbers))
        numbers.remove(max(numbers))

        media = sum(numbers) / len(numbers)

        print(f"\033[30mA \033[m\033[1;35mMédia\033[m\033[30m desses \033[m\033[1;36m{len(numbers)}\033[m\033[31m (Sem o Maior e o Menor)\033[m\033[30m Números aproximada é: \033[m\033[1;36m{media:.1f}\033[m")
    elif (choice == "15"): # Horas
        hours = float(input("\033[30mDigite a Quantidade de \033[m\033[1;32mHoras\033[m\033[30m: \033[m\033[1;36m"))
        minutes = (hours - trunc(hours)) * 60
        seconds = (minutes - trunc(minutes)) * 60

        print(f"\033[30m- \033[m\033[32m{trunc(hours)} Horas\033[m\033[30m e \033[m\033[33m{trunc(minutes)} Minutos\033[m\033[30m e \033[m\033[34m{trunc(seconds)} Segundos\033[m")
    elif (choice == "16"): # Área Dividida por 1,5
        area = float(input("\033[30mDigite a área: \033[m\033[1;36m"))

        print(f"\033[33mA \033[m\033[35mQuantidade de caixas\033[m\033[33m de 1.5m² necessárias é de: \033[m\033[1;32m{ceil(area / 1.5)} caixas\033[m")
    else:
        print("\033[1;31mOperação Inválida!\033[m")

if __name__ == "__main__":
    main()