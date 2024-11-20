from ast import literal_eval

print(" 1 - Saída 1 \n 2 - Soma de Matriz \n 3 - Média de Matriz \n 4 - Soma da Linha 2 da Matriz \n 5 - Soma da Última Linha da Matriz \n 6 - Soma da i Linha da Matriz \n 7 - Soma da segunda Coluna da Matriz \n 8 - Soma da última Coluna da Matriz \n 9 - Soma da i Coluna da Matriz \n 10 - Último Elemento da Matriz \n 11 - Index do Maior Elemento da Matriz \n 12 - Maior elemento de cada coluna")
choice: str = input("- Escolha uma Atividade Acima: ")
print("=" * 100)

match choice:
    case '1':
        a = [
            [2, 5, 0],
            [-1, 5, 3],
            [-2, 10, 9],
            [15, 20, 25]
        ]
        print(a[0][0]) # 2
        print(a[0][1]) # 5
        print(a[1][0]) # -1
        print(a[3][2]) # 25
        print(a[0][2] + 2) # 2
        print(a[3][0] + a[0][2]) # 15
        print(a[1][0] * a[2][1]) # -10
        print(a[1]) # [-1, 5, 3]
        print(len(a)) # 4
        print(len(a[2])) # 3

    case '2':
        def sum_matrix(matrix: list[list[int]]) -> int:
            total: int = 0
            total += sum([c for l in matrix for c in l if c % 2 == 0])
            return total

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(sum_matrix(matrix))

    case '3':
        def media_matrix(matrix: list[list[int]]) -> int | None:
            matrix_list: list[int] = [c for l in matrix for c in l]
            if len(matrix_list) == 0: return None
            return sum(matrix_list) / len(matrix_list)

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(media_matrix(matrix))

    case '4':
        def sum2_matrix(matrix: list[list[int]]) -> int:
            if len(matrix) < 2: return None
            total: int = sum(matrix[1])
            return total

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(sum2_matrix(matrix))

    case '5':
        def sumlast_matrix(matrix: list[list[int]]) -> int:
            if len(matrix) == 0: return None
            total: int = sum(matrix[-1])
            return total

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(sumlast_matrix(matrix))
    
    case '6':
        def sumi_matrix(matrix: list[list[int]], index: int) -> int:
            total: int = sum(matrix[index])
            return total

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        index: int = int(input("- Insira um Index da Matriz: "))
        print(sumi_matrix(matrix, index))
    
    case '7':
        def sum_c_matrix(matrix: list[list[int]]) -> int | None:
            if len(matrix) > 0 and len(matrix[0]) >= 2:
                return sum([l[1] for l in matrix])
            return None

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(sum_c_matrix(matrix))
    
    case '8':
        def sum_lastc_matrix(matrix: list[list[int]]) -> int | None:
            if len(matrix) > 0 and len(matrix[0]) > 0:
                return sum([l[-1] for l in matrix])
            return None

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        print(sum_lastc_matrix(matrix))
    
    case '9':
        def sum_ic_matrix(matrix: list[list[int]], index: int) -> int:
            return sum([l[index] for l in matrix])

        matrix: list[list[int]] = literal_eval(input("- Insira uma Matriz: "))
        index: int = int(input("- Insira um Index da Matriz: "))
        print(sum_ic_matrix(matrix, index))
    
    case '10':
        def laststr_matrix(matrix: list[list[str]], last_search: str) -> tuple[int, int] | None:
            last_index: tuple[int, int] = None
            for il, l in enumerate(matrix):
                for ic, c in enumerate(l):
                    if c == last_search: last_index = (il, ic)
            return last_index

        matrix: list[list[str]] = literal_eval(input("- Insira uma Matriz: "))
        last_search: str = input("- Insira um Elemento: ")
        print(laststr_matrix(matrix, last_search))
    
    case '11':
        def larger_element_matrix(matrix: list[list[str]]) -> tuple[int, int]:
            last_index: tuple[int, tuple[int]] = (0, (0, 0))

            for il, l in enumerate(matrix):
                for ic, c in enumerate(l):
                    if c > last_index[0]:
                        last_index = (c, (il, ic))
            
            return last_index[1]

        matrix: list[list[str]] = literal_eval(input("- Insira uma Matriz: "))
        print(larger_element_matrix(matrix))
    
    case '12':
        def large_c_matrix(matrix: list[list[str]]) -> tuple[int, int]:
            sums: list[int] = matrix[0]

            for l in range(1, len(matrix)):
                for ic, c in enumerate(matrix[l]):
                    sums[ic] = max(sums[0], c)
            
            return tuple(sums)

        matrix: list[list[str]] = literal_eval(input("- Insira uma Matriz: "))
        print(large_c_matrix(matrix))

    case _:
        print("Opção Inválida")