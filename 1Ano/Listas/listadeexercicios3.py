from ast import literal_eval
from random import randint

print(f"{"Lista de Exercícios 3 - ILP":^51}")
print("="*51)
print(" 1 - Saída 1 \n 2 - Saída 2 \n 3 - Saída 3 \n 4 - Saída 4 \n 5 - Saída 5 \n 6 - Saída 6 \n 7 - Saída 7 \n 8 - Saída 8 \n 9 - Saída 9 \n 10 - Saída 10 \n 11 - Média da Lista Input \n 12 - Soma dos Divisíveis por 3 \n 13 - Sublista de Divisíveis por 5 \n 14 - Elementos pares e indexes \n 15 - Menor elemento de uma lista \n 16 - Maior elemento de uma lista \n 17 - Menor e Maior elementos de uma lista \n 18 - Indexes do Menor e Maior elementos de uma lista \n 19 - Dobro de uma Lista \n 20 - Entradas Pares e Ímpares \n 21 - Valores e Média \n 22 - Números Pares e Ímpares Lidos \n 23 - 5 Números Aleatórios \n 24 - 10 Números Aleatórios e os Acima de 4 \n 25 - lista de n inteiros e ocorrências de a \n 26 - Números aleatórios e asteriscos \n 27 - Soma de Listas \n 28 - Interseção de duas listas \n 29 - União de duas listas \n 30 - Lista de forma intercalada \n 31 - Histograma de Asteriscos")
option: str = input(" - Selecione uma das opções Acima: ")

print("-"*51)

match option:
    case "1":
        L = [51, 8, 31, 11, 1, 56]
        el = 2
        print(L[0])                      # 51
        print(L[3])                      # 11
        print(L[el])                      # 31
        print(L[el + 1])                  # 11
        print(L[-1])                     # 56
        print(L[-3])                     # 11
        print(L[-el])                     # 1
        print(L[L[4]])                   # 8
        print(L[2] - L[-4])              # 0
    case "2":
        ls = [3, 5, 2]
        s = 0
        for v in ls:
            s = s + v
        print(s)                         # 10
    case "3":
        ls = [3, 5, 2, 10]
        p = 1
        for v in ls:
            p = p * v
        print(p)                         # 300
    case "4":
        n = 6
        ls = [0] * n
        for el in range(n):
            ls[el] = el * 2
        print(ls)                        # [0, 2, 4, 6, 8, 10]
    case "5":
        n = 5
        ls = []
        for el in range(n):
            ls.append(1)
        ls[0] = 5
        ls[3] = -3
        print(ls)                        # [5, 1, 1, -3, 1]
    case "6":
        ls = [3, 5, 2, 10, 9, 1]
        s = 0
        for el in range(0, len(ls), 2):
            s = s + ls[el]
        print(s)                         # 14
    case "7":
        n = 5
        ls = [None] * n
        for el in range(n):
            ls.append(1)
        ls[0] = 5
        ls[3] = -3
        print(ls)                        # [5, None, None, -3, None, 1, 1, 1, 1, 1]
    case "8":
        la = ['A', 'B', 'C']
        lb = [4, 2, 3]
        for el in range(len(la)):
            print(la[el] * lb[el])         # AAAA \n BB \n CCC
    case "9":
        la = [0, 5, 8]
        lb = [4, 2, 3]
        lc = []
        for el in range(len(la)):
            v = la[el] + lb[el]
            lc.append(v)
        print(lc)                        # [4, 7, 11]
    case "10":
        la = [0, 5, 3, -1, 2]
        sp = 0
        si = 0
        el = 0
        while el < len(la):
            if el % 2 == 0:
                sp += la[el]
            else:
                si += la[el]
            el += 1
        print(sp)                        # 5
        print(si)                        # 4
    case "11":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        print(f"Média: {sum(list_input)/len(list_input)}")
    case "12":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        list_mod3: list[int] = [num for num in list_input if num % 3 == 0]
        print(f"Soma dos divisíveis por 3: {sum(list_mod3)}")
    case "13":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        list_mod5: list[int] = [num for num in list_input if num % 5 == 0]
        print(f"Sublista dos Divisíveis por 5: {list_mod5}")
    case "14":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        dict_even: dict[int, int] = {num : index for num, index in zip(list_input, range(len(list_input))) if num % 2 == 0}
        print("Elemento Índice")
        print("-------- ------")
        for el in dict_even:
            print(f"{el:<8} {dict_even[el]:<6}")
    case "15":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        print(f"Menor elemento: {min(list_input)}")
    case "16":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        print(f"Maior elemento: {max(list_input)}")
    case "17":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        print(f"Menor elemento: {min(list_input)}")
        print(f"Maior elemento: {max(list_input)}")
    case "18":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        print(f"Índex do Menor elemento: {list_input.index(min(list_input))}")
        print(f"Índex do Maior elemento: {list_input.index(max(list_input))}")
    case "19":
        list_input: list[int] = literal_eval(input("- Digite uma Lista de inteiros: "))
        list_double: list[int] = [num * 2 for num in list_input]
        print(list_double)
    case "20":
        list_even: list[int] = []
        list_odd: list[int] = []
        for _ in range(4):
            value_input: int = int(input())
            if value_input % 2 == 0: list_even.append(value_input)
            else: list_odd.append(value_input)
        print(f"Pares: {list_even}")
        print(f"Ímpares: {list_odd}")
    case "21":
        values: list[int] = [int(input()) for _ in range(5)]
        average: int = sum(values) // len(values)
        greater_average: list[int] = [num for num in values if num > average]
        lower_average: list[int] = [num for num in values if num < average]
        print(f"Média: {average}")
        print(f"Valores acima da média: {greater_average}")
        print(f"Valores abaixo da média: {lower_average}")
    case "22":
        actual_number: int = 1
        numbers: list[int] = []
        while actual_number > 0:
            actual_number = int(input())
            numbers.append(actual_number)
        even_numbers: list[int] = [num for num in numbers if num % 2 == 0]
        odd_numbers: list[int] = [num for num in numbers if num % 2 != 0]
        print(f"Pares: {even_numbers}")
        print(f"Ímpares: {odd_numbers}")
    case "23":
        random_numbers: list[int] = [randint(0, 9) for _ in range(5)]
        print(random_numbers)
    case "24":
        random_numbers: list[int] = [randint(-10, 10) for _ in range(10)]
        greater_four: list[int] = [num for num in random_numbers if num > 4]
        print(f"Lista: {random_numbers}")
        print(f"Acima de quatro: {greater_four}")
    case "25":
        n: int = int(input(" - Digite um inteiro não negativo: "))
        a: int = int(input(" - Digite um elemento para saber a quantidade de ocorrências: "))
        random_numbers: list[int] = [randint(0, 15) for _ in range(n)]
        count_a: int = random_numbers.count(a)
        print(random_numbers)
        print(f"{count_a} ocorrência(s) de {a}")
    case "26":
        random_numbers: list[int] = [randint(1, 5) for _ in range(10)]
        asterisk_on_three: list[int | str] = [i if i != 3 else "*" for i in random_numbers]
        asterisk_on_not_three: list[int | str] = [i if i == 3 else "*" for i in random_numbers]
        print(asterisk_on_three)
        print(asterisk_on_not_three)
    case "27":
        random_list1: list[int] = [randint(-5, 5) for _ in range(6)]
        random_list2: list[int] = [randint(-5, 5) for _ in range(6)]
        sum_random_lists: list[int] = [x+y for x, y in zip(random_list1, random_list2)]
        print(random_list1)
        print(f"{"+":^{len(str(random_list1))}}")
        print(random_list2)
        print(f"{"=":^{len(str(random_list2))}}")
        print(sum_random_lists)
    case "28":
        user_list: list[int] = [int(input()) for _ in range(5)]
        random_list: list[int] = [randint(1, 9) for _ in range(5)]
        intersection_list: list[int] = set(user_list) & set(random_list)
        print(user_list)
        print(random_list)
        print(f"Interseção: {list(intersection_list)}")
    case "29":
        user_list: list[int] = [int(input()) for _ in range(5)]
        random_list: list[int] = [randint(1, 9) for _ in range(5)]
        union_list: list[int] = set(user_list) | set(random_list)
        print(user_list)
        print(random_list)
        print(f"Interseção: {list(union_list)}")
    case "30":
        user_list: list[int] = [int(input()) for _ in range(4)]
        random_list: list[int] = [randint(1, 9) for _ in range(4)]
        interleaved_list: list[int] = []
        for i in range(4):
            interleaved_list.append(user_list[i])
            interleaved_list.append(random_list[i])
        print(user_list)
        print(random_list)
        print(interleaved_list)
    case "31":
        histogram: list[int] = [""] * 10
        for _ in range(90):
            actual_number: int = randint(0, 9)
            histogram[actual_number] += "*"
        for index, asterisks in enumerate(histogram):
            print(f"{index} : {asterisks}")
    case _: print("Opção Inválida!")