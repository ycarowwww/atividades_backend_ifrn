from re import findall as re_findall

print("Lista 02 de POO")
print("-" * 50)
print("1 - Inteiros em ordem crescente\n2 - Inteiros em ordem decrescente\n3 - Inteiros com valores invertidos\n4 - Inteiros com valores invertidos 2\n5 - Valores somados\n6 - Números com 3 valores anteriores somados\n7 - Frases a partir de uma frase\n8 - Últimas letras\n9 - Frase repetida\n10 - Strings a partir de uma string\n11 - Soma dos algarismos\n12 - Quantidade de Palavras\n13 - Palavra Invertida\n14 - Palavras Invertidas\n15 - Senha a partir de uma frase\n16 - Quantidade de Vogais\n17 - Palavras Repetidas\n18 - Sequência de Números\n19 - Tabuada\n20 - Sequência de Números")
option: str = input("Selecione uma Opção acima: ")

print("-" * 50)
match option:
    case "1":
        print(f"Resultado: {' '.join([ str(i) for i in range(1, 11) ])}")
    case "2":
        print(f"Resultado: {' '.join([ str(i) for i in range(10, 0, -1) ])}")
    case "3":
        print(f"Resultado: {' '.join([ str(i * (-1 if i % 2 == 0 else 1)) for i in range(1, 11) ])}")
    case "4":
        print(f"Resultado: {' '.join([ str(i * (-1 if i % 3 == 0 else 1)) for i in range(1, 31) ])}")
    case "5":
        nums = [ 1 ]
        for i in range(1, 10):
            nums.append(nums[-1] + i)
        print(f"Resultado: {' '.join([ str(n) for n in nums ])}")
    case "6":
        nums: list[int] = [ ]
        for i in range(30):
            if i % 3 == 0 and i > 0:
                nums.append(nums[-1] + nums[-2] + nums[-3])
            nums.append(i+1)
        nums.append(nums[-1] + nums[-2] + nums[-3])
        print(" ".join([ str(n) for n in nums ]))
    case "7":
        phrase = input("Digite uma fase:\n").split()

        for _ in range(len(phrase)):
            print(" ".join(phrase))
            phrase.pop(0)
    case "8":
        last_letters = [ i[-1] for i in input("Digite uma fase:\n").split() ]

        print("".join(last_letters))
    case "9":
        phrase = input("Digite uma frase: ")

        for i in range(len(phrase)):
            print(f"{i+1} - {phrase}")
    case "10":
        phrase = list(input("Digite uma frase:\n"))

        for i in range(len(phrase)):
            letter = phrase.pop(0)
            phrase.append(letter)
            print("".join(phrase))
    case "11":
        phrase_algarisms = [ int(i) for i in input("Digite uma frase:\n") if i in "0123456789" ]

        print(sum(phrase_algarisms))
    case "12":
        phrase = input("Digite uma frase:\n").split()

        print(len(phrase))
    case "13":
        phrase = input("Digite uma frase:\n")

        print(phrase[::-1])
    case "14":
        phrase = input("Digite uma frase:\n").split()

        for w in phrase:
            print(w[::-1])
    case "15":
        phrase_lens = [ str(len(i)) for i in input("Digite uma frase:\n").split() ]

        print("".join(phrase_lens))
    case "16":
        phrase = input("Digite uma frase:\n").lower()

        for letter in "aeiou":
            print(f"{letter.upper()} - {phrase.count(letter)}")
    case "17":
        phrase = input("Digite uma frase:\n").lower().split()
        phrase_counts: list[int] = [ ]

        for w in phrase:
            phrase_counts.append(len(re_findall(r"[aeiou]", w)))
        
        for i in range(len(phrase)):
            for _ in range(phrase_counts[i]):
                print(phrase[i], end=" ")
    case "18":
        nums = list(map(int, input("Digite uma sequência de números separados por vírgula:\n").split(",")))

        print(f"Soma = {sum(nums)}")
    case "19":
        for i in range(1, 11):
            print(f"\nTabuada do {i}\n")
            for j in range(1, 11):
                print(f"{i} x {j} = {i * j}")
    case "20":
        for i in range(1, 11):
            print(i, end=" ")
            for j in range(2, i+1, 2):
                print(j, end=" ")
            print()
    case _:
        print("Opção Inválida!")
