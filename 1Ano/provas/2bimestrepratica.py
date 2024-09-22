number: int = int(input())
for n in range(1, number+1):
    print(f'{number} / {n} = {'não é um número inteiro' if number / n != number // n else int(number / n)}')