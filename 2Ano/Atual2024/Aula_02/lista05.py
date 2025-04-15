print("Lista 05 de POO")
print("-" * 50)
print("1 - Maior entre 2\n2 - Maior entre 3\n3 - Inicias de um Nome\n4 - Aluno Aprovado\n5 - Iniciais em Maiusculo")
option: str = input("Selecione uma Opção acima: ")

def maior2(x: int, y: int) -> int: return max(x, y)

def maior3(x: int, y: int, z: int) -> int: return max(x, y, z)

def iniciais(nome: str) -> str:
    letras: list[str] = []

    for p in nome.split():
        letras.append(p[0])
    
    return "".join(letras)

def aprovado(nota1: int, nota2: int) -> bool:
    mean: int = round((nota1 * 2 + nota2 * 3) / 5)
    return mean >= 60

def formatar_nome(nome: str) -> str:
    return " ".join([ word.capitalize() for word in nome.lower().split() ])

print("-" * 50)
match option:
    case "1":
        num1, num2 = [ int(i) for i in input("Números [x y]: ").split() ]
        print(maior2(num1, num2))
    case "2":
        num1, num2, num3 = [ int(i) for i in input("Números [x y z]: ").split() ]
        print(maior3(num1, num2, num3))
    case "3":
        name: str = input("Digite seu Nome: ")
        print(iniciais(name))
    case "4":
        grade_1: int = int(input("Digite a nota do primeiro bimestre da disciplina: "))
        grade_2: int = int(input("Digite a nota do segundo bimestre da disciplina: "))
        
        print(f"Passou?: {aprovado(grade_1, grade_2)}")
    case "5":
        name: str = input("Digite seu Nome: ")
        print(formatar_nome(name))
    case _:
        print("Opção Inválida!")
