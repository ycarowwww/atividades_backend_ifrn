from ast import literal_eval

print(f"{"\033[1;33mLista de Exercícios 5 - ILP\033[m":^51}")
print("\033[30m=\033[m"*51)
print(" 1 - Saída 1 \n 2 - Saída 2 \n 3 - Saída 3 \n 4 - Saída 4 \n 5 - Saída 5 \n 6 - Saída 6 \n 7 - Saída 7 \n 8 - Saída 8 \n 9 - Saída 9 \n 10 - Números Pares da Matriz \n 11 - Maior Número de cada linha \n 12 - Maior e Menor da Matriz \n 13 - Diagonais da Matriz \n 14 - Elementos menos a Diagonal Principal")
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

    # Falta ainda os de 15 até 25

    case _: print("\033[31mOpção Inválida!\033[m")