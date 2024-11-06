print(" 1 - Saída Fatiamento de Lista")
choice: str = input("- Escolha uma Atividade Acima: ")
print("=" * 100)

match choice:
    case '1':
        L = [5, 0, 3, 8, 9, 4, 1, 2]

        print(L[0:])
        print(L[:5])
        print(L[2:7])
        print(L[3:4])
        print(L[-7:-3])
        print(L[:15])
        print(L[::2])
        print(L[1::3])
        print(L[-2::-1])
    case _:
        print("Opção Inválida")