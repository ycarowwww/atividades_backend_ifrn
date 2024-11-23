from ast import literal_eval
from typing import Any
from random import randint

print(f"{"\033[1;33mLista de Exercícios 5 - ILP\033[m":^51}")
print("\033[30m=\033[m"*51)
print(" 1 - Saída 1 \n 2 - Saída 2 \n 3 - Saída 3 \n 4 - Saída 4 \n 5 - Saída 5 \n 6 - Saída 6 \n 7 - Saída 7 \n 8 - Saída 8 \n 9 - Saída 9 \n 10 - Números Pares da Matriz \n 11 - Maior Número de cada linha \n 12 - Maior e Menor da Matriz \n 13 - Diagonais da Matriz \n 14 - Elementos menos a Diagonal Principal \n 15 - Transposição de Matriz \n 16 - Triangularização Superior da Matriz \n 17 - Saída 10 \n 18 - Saída 11 \n 19 - Saída 12 \n 20 - Atribuição de Elementos ao Cubo \n 21 - Associação de A a B \n 22 - Elementos de um Dicionário \n 23 - Maiores Chaves \n 24 - Teorema do Limite Central \n 25 - Aplicativo de Mercearia")
option: str = input("\033[32m - Selecione uma das opções Acima: \033[31m\033[34m")

print("\033[30m-\033[m"*51)

match option:
    case "1":
        m = [
            [5, 2, 1, -1, 3],
            [7, 4, 6, 3, -2],
            [-8, 4, 2, 9, 0]
        ]
        x = 0
        y = 2
        print(m[0][1])
        print(m[2][3])
        print(m[x][y])
        print(m[y][x])
        print(m[x + 1][y - 1])
        z = m[0][2]
        print(m[z][y * 2])
        print(m[2][4] + x)
        print(m[2][4] + m[0][3])
        u = m[m[2][2]][y]
        print(u)
    
    case "2":
        m = [
            [5, 2],
            [7, -4],
            [-8, 4]
        ]
        for L in m:
            print(L)

    case "3":
        m = [
            [5, 2, 0],
            [7, -4, 9],
            [-8, 4, 3]
        ]
        for L in m:
            print(L[2])

    case "4":
        m = [[5, 2, 0], [7, -4, -9], [-8, 4, 0]]
        for L in m:
            for v in L:
                if v > 0:
                    print(v)

    case "5":
        m = [
            [5, 2, 0, 7, -4, -9],
            [-8, 4, 0, 6, 6, 3]
        ]
        for i, L in enumerate(m):
            for j, v in enumerate(L):
                if v % 2 != 0:
                    t = (i, j)
                    print(t)

    case "6":
        m = [
            [5, 2, 0, 7, -4, -9],
            [-8, 4, 0, 6, 6, 3]
        ]
        L = []
        for i in range(len(m)):
            for j in range(len(m[0])):
                v = m[i][j]
                if v > 5:
                    t = (i, j)
                    L.append(t)
        print(L)

    case "7":
        m = [[5, 2], [0, 7], [-4, -9], [-8, 4]]
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j] < 0:
                    m[i][j] = 0
        print(m)

    case "8":
        m = [
            [5, 2, 0, 7, 9],
            [-4, -9, -8, 4, 8]
        ]
        i = 0
        for L in m:
            for v in L:
                if i % 3 == 0:
                    print(v)
                i += 1

    case "9":
        A = [
            [5, 2, 0, 1],
            [-4, -9, 8],
            [10, 11, 12, 20]
        ]
        B = [2, 4, 6, 8]
        r = []
        for v in B:
            for L in A:
                if v in L:
                    r.append(v)
        print(r)

    case "10":
        def even_numbers_matrix(matrix: list[list[int]]) -> list[int]:
            even_numbers: list[int] = [j for i in matrix for j in i if j % 2 == 0]
            return even_numbers

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(even_numbers_matrix(matrix))

    case "11":
        def larger_number_lines(matrix: list[list[int]]) -> list[int]:
            numbers: list[int] = [max(l) for l in matrix if len(l) > 0]
            return numbers

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(larger_number_lines(matrix))
    
    case "12":
        def extremes_number_lines(matrix: list[list[int]]) -> tuple[int, int] | None:
            larger_numbers: list[int] = [max(l) for l in matrix if len(l) > 0]
            smaller_numbers: list[int] = [min(l) for l in matrix if len(l) > 0]
            if len(larger_numbers) == 0 or len(smaller_numbers) == 0:
                return None
            return (min(smaller_numbers), max(larger_numbers))

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(extremes_number_lines(matrix))

    case "13":
        def diagonals_matrix(matrix: list[list[int]]) -> tuple[list[int], list[int]] | None:
            for l in matrix:
                if len(l) != len(matrix):
                    return None
            if len(matrix) == 0:
                return None
            
            main_diagonal: list[int] = [matrix[el][el] for el in range(len(matrix))]
            seco_diagonal: list[int] = [matrix[i][j] for i, j in zip(range(len(matrix) - 1, -1, -1), range(len(matrix)))]

            return (main_diagonal, seco_diagonal)

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(diagonals_matrix(matrix))
    
    case "14":
        def indiagonal_matrix(matrix: list[list[int]]) -> list[int]:
            if len(matrix) == 0 or len(matrix) != len(matrix[0]): 
                return []
            
            numbers: list[int] = []
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if i != j:
                        numbers.append(matrix[i][j])
            
            return numbers

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(indiagonal_matrix(matrix))
    
    case "15":
        def transposition_matrix(matrix: list[list[int]]) -> list[list[int]] | None:
            if len(matrix) == 0: 
                return None
            
            new_matrix: list[list[int]] = []

            for _ in range(len(matrix[0])):
                new_matrix.append([])
            
            for l in range(len(matrix)):
                for c in range(len(matrix[l])):
                    new_matrix[c].append(matrix[l][c])
            
            return new_matrix

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(transposition_matrix(matrix))

    case "16":
        def check_quadralization(matrix: list[list[int]]) -> bool:
            for l in matrix:
                if len(l) != len(matrix):
                    return False
            return True
        
        def triangularization_matrix(matrix: list[list[int]]) -> bool | None:
            if len(matrix) == 0 or not check_quadralization(matrix):
                return None
            
            for l in range(len(matrix)):
                for c in range(l + 1, len(matrix[l])):
                    if matrix[l][c] != 0:
                        return False
            
            return True

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(triangularization_matrix(matrix))
    
    case "17":
        d = {'a': 5, 'b': 11, 'c': 3}
        for c, v in d.items():
            print(f'{c}, {v}')
        print(d.get('c'))
        print(d.get('d'))
        print('a' in d)
        print(11 in d)
        d.pop('b')
        print(len(d))

    case "18":
        L = ['casa', 'bola', 'peixe']
        d = {}
        for i, v in enumerate(L):
            d[i] = v
        d['casa'] = 10
        d[1] = 'praia'
        for c, v in d.items():
            print(f'{c} : {v}')

    case "19":
        A = ['casa', 'bola', 'peixe', 'pão']
        B = ['ana', 'paula', 'pedro', 'alex']
        n = len(A)
        d = {}
        for i in range(n):
            j = n - i - 1
            c = B[i]
            v = A[j]
            d[c] = v
        print(d)

    case "20":
        def cubic_elements(n: int) -> dict[int, int]:
            if n < 3:
                return {}
            
            new_dict: dict[int, int] = {}
            
            for i in range(2, n + 1):
                new_dict[i] = i ** 3

            return new_dict
        
        number: int = int(input("- Insira um Número: "))
        print(cubic_elements(number))

    case "21":
        def association_a_b(A: list[Any], B: list[Any]) -> dict[Any, Any]:
            return {a : b for a, b in zip(A, B)}
        
        set_a: list[Any] = literal_eval(input("- Insira uma Lista: "))
        set_b: list[Any] = literal_eval(input("- Insira uma Lista: "))
        print(association_a_b(set_a, set_b))

    case "22":
        def dict_elements_set(dictionary: dict[Any, Any]) -> list[Any]:
            return list(set([i for i in dictionary.values()]))
        
        dict_a: dict[Any, Any] = literal_eval(input("- Insira um Dicionário: "))
        print(dict_elements_set(dict_a))

    case "23":
        def larger_key(dictionary: dict[int, int]) -> list[int]:
            item: list[list[int], int] = [[]]

            for i, e in dictionary.items():
                if len(item) == 1:
                    item[0].append(i)
                    item.append(e)

                if e > item[1]:
                    item[1] = e
                    item[0] = [i]
                elif e == item[1]:
                    item[0].append(i)
            
            return item[0]
        
        dict_a: list[Any] = literal_eval(input("- Insira um Dicionário: "))
        print(larger_key(dict_a))

    case "24":
        end_point1: int = int(input("\033[m- Insira o \033[35mLimite 1\033[m: \033[36m"))
        end_point2: int = int(input("\033[m- Insira o \033[34mLimite 2\033[m: \033[36m"))
        amount: int = int(input("\033[m- Insira a \033[33mQuantidade de Números\033[m: \033[36m"))

        rnd_numbers: dict[int, int] = { n : 0 for n in range(end_point1, end_point2 + 1) }
        for _ in range(amount):
            rnd_numbers[randint(end_point1, end_point2)] += 1

        for i, e in rnd_numbers.items():
            print(f"\033[33m{i}\033[m - \033[36m{'*' * e}\033[m")

    case "25":
        products: list[tuple[str, float]] = [
            ("palma de banana", 4.00),
            ("unidade de abacaxi", 3.00),
            ("unidade de melão", 2.50),
            ("quilo de abacate", 5.50)
        ]

        main_option: str = ""
        seco_option: str = ""
        total: float = 0.00
        bought_summarize: list[str] = []

        while True:
            print("1 - iniciar nova venda \n2 - sair")
            main_option = input("Informe a opção desejada: ")

            match main_option:
                case "1":
                    while True:
                        print("0 - encerrar compra")
                        print(*[f"{p + 1} - {products[p][0]:<20} R${products[p][1]:.2f}" for p in range(len(products))], sep="\n")
                        seco_option = input("Informe a opção desejada: ")

                        match seco_option:
                            case "0":
                                break
                            
                            case seco_option if int(seco_option) <= len(products):
                                amount: int = int(input("Informe a quantidade: "))
                                product: tuple[str, float] = products[int(seco_option) - 1]
                                total += product[1] * amount
                                bought_summarize.append(f"{product[0]}, {amount:.1f}, R${(product[1] * amount):.2f}")
                                print(f"Resumo da compra: ")
                                for s in bought_summarize: print(f" {s}")
                                print(f" TOTAL: R${total:.2f}")

                            case _:
                                print("Opção Inválida")

                case "2":
                    break

                case _:
                    print("Opção Inválida!")

    case _: print("\033[31mOpção Inválida!\033[m")
