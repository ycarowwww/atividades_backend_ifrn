print(" 1 - Saída Fatiamento de Lista")
choice: str = input("- Escolha uma Atividade Acima: ")
print("=" * 100)

match choice:
    case '1':
        L = [5, 0, 3, 8, 9, 4, 1, 2]

        print(L[0:])     # [5, 0, 3, 8, 9, 4, 1, 2]
        print(L[:5])     # [5, 0, 3, 8, 9]
        print(L[2:7])    # [3, 8, 9, 4, 1]
        print(L[3:4])    # [8]
        print(L[-7:-3])  # [0, 3, 8, 9]
        print(L[:15])    # [5, 0, 3, 8, 9, 4, 1, 2]
        print(L[::2])    # [5, 3, 9, 1]
        print(L[1::3])   # [0, 9, 2]
        print(L[-2::-1]) # [1, 4, 9, 8, 3, 0, 5]
    case _:
        print("Opção Inválida")