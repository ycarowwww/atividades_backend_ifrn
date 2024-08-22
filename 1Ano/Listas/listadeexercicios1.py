print(" 1 - Dobro \n 2 - Soma de 3 \n 3 - Média de 3 \n 4 - Output 1 \n 5 - Output 2 \n 6 - Output 3 \n 7 - Divisão e Resto de 2 Números \n 8 - Bolos que podem ser comprados \n 9 - Bandeirada \n 10 - Intervalo 0 e 6 \n 11 - Intervalo 0 e 10 \n 12 - Múltiplo de 5 \n 13 - Múltiplo de 5 ou 3 \n 14 - Notas de Alunos \n 15 - Múltiplo de 5 e 3 \n 16 - Corrida / Tempo \n 17 - Horários \n 18 - Output 4 \n 19 - Output 5 \n 20 - Output 6 \n 21 - Output 7")
choice = input("- Escolha uma das Opções acima: ")

print("=" * 50)

if (choice == "1"):
    n1 = int(input("- Digite um Número: "))
    print(f"O Dobro de {n1} é: {n1 * 2}")
elif (choice == "2"):
    n1 = int(input("- Digite um Número: "))
    n2 = int(input("- Digite um outro Número: "))
    n3 = int(input("- Digite um outro Número: "))
    print(f"A Soma deles é: {n1+n2+n3}")
elif (choice == "3"):
    n1 = float(input("- Digite um Número: "))
    n2 = float(input("- Digite um outro Número: "))
    n3 = float(input("- Digite um outro Número: "))
    print(f"A Média deles é: {(n1+n2+n3)/3}")
elif (choice == "4"):
    a = 2
    b = 3
    c = -1
    x = a + b * c
    print(x)
elif (choice == "5"):
    a = 10
    b = 5
    c = a * b
    c = c % 3
    print(c)
elif (choice == "6"):
    a = 4
    b = a * 2
    print(a)
    print(b)
    print('----')
    c = a
    a = b
    b = c
    print(a)
    print(b)
elif (choice == "7"):
    n1 = float(input("- Digite um Número: "))
    n2 = float(input("- Digite um outro Número: "))
    print(f"O Quociente: {n1 // n2} \nO Resto: {n1 % n2}")
elif (choice == "8"):
    money = float(input("- Digite a quantidade de Dinheiro: "))
    cake = 8.50
    units = money // cake
    change = money - (cake * units)
    print(f"É possível comprar {units} bolos \nO troco será de: R${change:.2f}")
elif (choice == "9"):
    flags = {
        1 : 3.00,
        2 : 4.18
    }
    print(" - Bandeira 1 - R$3.00 \n - Bandeira 2 - R$4.18")
    flag = int(input("- Escolha uma das Bandeiras: "))
    distance = float(input("- Digite a Distância (km): "))
    flagged = 4.85
    if (1 <= flag <= 2):
        print(f"O Preço será de : {distance * flags[flag] + flagged}")
    else:
        print("Bandeira Inválida!")
elif (choice == "10"):
    n = int(input("- Digite um Número Inteiro: "))

    print(0 <= n <= 6)
elif (choice == "11"):
    n = int(input("- Digite um Número Inteiro: "))

    print(not 0 < n < 10)
elif (choice == "12"):
    n = int(input("- Digite um Número Inteiro: "))

    if (n % 5 == 0):
        print(f"{n} é múltiplo de 5")
    else:
        print(f"{n} não é múltiplo de 5")
elif (choice == "13"):
    n = int(input("- Digite um Número Inteiro: "))

    m5 = n % 5 == 0
    m3 = n % 3 == 0

    print(f" - Múltiplo de 3: {m3} \n - Múltiplo de 5: {m5}")
elif (choice == "14"):
    n = []
    for i in range(3):
        n.append(int(input(f"- Digite a Nota {i + 1}: ")))
    media = int(sum(n)/len(n))

    print(f"Média: {media}")
    if (media < 30):
        print("Resultado: Reprovado")
    elif (29 < media < 70):
        print("Resultado: Em Recuperação")
    else:
        print("Resultado: Aprovado")
elif (choice == "15"):
    n = int(input("- Digite um Número Inteiro: "))

    if (n % 15 == 0):
        print(f"{n} é múltiplo de 5 e 3")
    else:
        print(f"{n} não é múltiplo de 5 e 3")
elif (choice == "16"):
    st_h = int(input("- Horas do Início: "))
    st_m = int(input("- Minutos do Início: "))
    fi_h = int(input("- Horas da Finalização: "))
    fi_m = int(input("- Minutos da Finalização: "))
    t_st = st_h * 60 + st_m
    t_fi = fi_h * 60 + fi_m

    if (t_st > t_fi):
        t_fi += 1440
    
    t = abs(t_st - t_fi)

    print(f"A Corrida terminou às: \n {t // 60}h:{t % 60}min")
elif (choice == "17"):
    h = {
        "M" : "Matutino",
        "V" : "Vespertino",
        "N" : "Noturno"
    }

    l = input("Digite uma Letra [M, V, N]: ")
    print(f"Horário: {h.get(l, "Inválido")}")
elif (choice == "18"):
    x = int(input())
    y = x * 2
    if x > 0:
        y = y + 5
    print(y)
    
    # 2  > 9
    # -3 > -6
elif (choice == "19"):
    x = int(input())
    if x > 0 and x % 2 == 0:
        print("A")
    else:
        print("B")

    # 6  > A
    # 3  > B
    # -5 > B
elif (choice == "20"):
    x = int(input())
    print("A")
    if x == 11 or x % 3 == 0:
        print("B")
    else:
        print("C")
    print("D")

    # 11 > A B D
    # 12 > A B D
    # 0  > A B D
    # 17 > A C D
elif (choice == "21"):
    x = int(input())
    y = int(input())
    if y == 0:
        print(x)
    elif y == 1:
        print(x + 2)
    elif y == 2:
        print(x * 3)
    else:
        print(0)
    
    # 5 e 0  > 5
    # 3 e 2  > 9
    # 7 e 10 > 0
    # 1 e 1  > 3
else:
    print("Opção Inválida!")