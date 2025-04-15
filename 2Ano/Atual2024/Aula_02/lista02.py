print("Lista 02 de POO")
print("-" * 50)
print("1 - Nome Completo\n2 - Média Parcial\n3 - Características do Retângilo\n4 - Última palavra")
option: str = input("Selecione uma Opção acima: ")

print("-" * 50)
match option:
    case "1":
        name: str = input("Digite seu nome completo:\n")
        first_name = name.split()[0]
        print(f"\nBem-vindo(a) ao Python, {first_name}")
    case "2":
        grade_1: int = int(input("Digite a nota do primeiro bimestre da disciplina:\n"))
        grade_2: int = int(input("Digite a nota do segundo bimestre da disciplina:\n"))
        mean: int = round((grade_1 * 2 + grade_2 * 3) / 5)

        print(f"\nMédia parcial = {mean}")
    case "3":
        print("Digite a base e a altura do retângulo")
        base: float = float(input())
        height: float = float(input())
        
        area: float = base * height
        perimeter: float = (base + height) * 2
        diagonal: float = (base ** 2 + height ** 2) ** (1 / 2)

        print(f"Área = {area:.2f} - Perímetro = {perimeter:.2f} - Diagonal = {diagonal:.2f}")
    case "4":
        phrase: str = input("Digite uma frase:\n")

        last_index: int = phrase.rfind(" ")
        print(phrase[last_index+1:])
    case _:
        print("Opção Inválida!")
