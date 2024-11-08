print(" 1 - Saída Conjuntos \n 2 - Saída Dicionários")
choice: str = input("- Escolha uma Atividade Acima: ")
print("=" * 100)

match choice:
    case '1':
        s1 = {1, 0, 2, 8, 1, 9}
        s1.add(5)
        s1.add(0)
        print(s1) # {1, 0, 2, 8, 9, 5}
        s1.remove(9)  
        s1.discard(0)
        s1.discard(-2)
        print(s1) # {1, 2, 8, 5}
    case '2':
        d = {}
        d["a"] = 15
        d["b"] = None
        d["c"] = 3
        d["d"] = d["a"] / d["c"]
        print(d) # {'a':15, 'b':None, 'c':3, 'd':5.0}
        d["b"] = -2
        d.pop("c")
        print("c" in d) # False
        print(d) # {'a':15, 'b':-2, 'd':5.0}
    case _:
        print("Opção Inválida")