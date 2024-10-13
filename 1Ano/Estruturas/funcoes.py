from ast import literal_eval

print(" 1 - Multiplicação de 2 Números \n 2 - Par ou Ímpar \n 3 - Soma de 1 a N \n 4 - Soma de uma Lista de Números \n 5 - 0 em uma Lista de Números \n 6 - N ocorrências em uma Lista de Números \n 7 - Dobrar Lista")
choice: str = input("- Escolha uma Atividade Acima: ")
print("=" * 100)

match choice:
    case '1':
        def mult(a: int, b: int) -> int:
            return a * b
        
        numbers: list[int] = [int(input()) for _ in range(2)]
        print(f"Resultado: {mult(*numbers)}")
    case '2':
        def par_impar(a: int) -> str:
            return "Par" if a % 2 == 0 else "Ímpar"
        
        print(par_impar(int(input("Número: "))))
    case '3':
        def soma_1_n(n: int) -> int:
            return n * (n + 1) // 2

        number: int = int(input("Digite um Número: "))
        print(f"Soma de 1 a {number}: {soma_1_n(number)}")
    case '4':
        def soma_lista(nums: list[int]) -> int:
            return sum(nums)
        
        numbers: list[int] = literal_eval(input("- Digite uma lista de Números: "))
        print(f"Soma: {soma_lista(numbers)}")
    case '5':
        def ocorrencias_0(nums: list[int]) -> int:
            return nums.count(0)
        
        numbers: list[int] = literal_eval(input("- Digite uma lista de Números: "))
        print(f"Quantidade de 0s: {ocorrencias_0(numbers)}")
    case '6':
        def ocorrencias_num(nums: list[int], search_num: int) -> int:
            return nums.count(search_num)
        
        numbers: list[int] = literal_eval(input("- Digite uma lista de Números: "))
        search_number: int = int(input("- Digite um Número para Procurar: "))
        print(f"Quantidade de {search_number}s: {ocorrencias_num(numbers, search_number)}")
    case '7':
        def dobrar_lista(nums: list[int]) -> list[int]:
            return [2 * n for n in nums]

        numbers: list[int] = literal_eval(input("- Digite uma lista de Números: "))
        print(f"Lista Dobrada: {dobrar_lista(numbers)}")
    case _:
        print("Opção Inválida!")