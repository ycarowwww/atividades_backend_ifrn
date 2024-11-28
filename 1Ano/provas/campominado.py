from random import randint

# Falta ainda algumas coisas, além de melhorar essa porcaria

size = int(input("Size: "))
matrix = [[0 for _ in range(size)] for _ in range(size)]
bombs = 3

def increase_adjacents(matrix: list[list[int]], bomb: tuple[int, int]) -> None:
    for i in range(-1, 2):
        for j in range(-1, 2):
            pos: tuple[int, int] = (i + bomb[0], j + bomb[1])
            if 0 <= pos[0] < size and 0 <= pos[1] < size and matrix[pos[0]][pos[1]] != -1:
                matrix[pos[0]][pos[1]] += 1

for _ in range(bombs):
    pos = (randint(0, size-1), randint(0, size-1))
    while matrix[pos[0]][pos[1]] == -1:
        pos = (randint(0, size-1), randint(0, size-1))
    matrix[pos[0]][pos[1]] = -1
    increase_adjacents(matrix, pos)

def print_matrix(matrix: list[list[int]]) -> None:
    print(f" {'-':<{len(str(len(matrix)))}} ", end="|")

    for i in range(1, len(matrix[0])+1):
        print(f" {i:<{len(str(i))+1}} ", end="|")
    print()

    for il, l in enumerate(matrix):
        print(f" {str(il+1):<{len(str(len(matrix)))}} ", end="|")

        for ic, c in enumerate(l):
            print(f" {c:<{len(str(ic+1))+1}} ", end="|")
        print()

def check_empty_spaces(matrix: list[list[str]]) -> int:
    amount = 0
    for i in matrix:
        for j in i:
            if j == " ":
                amount += 1
    return amount

def valid_adjacents(matrix: list[list[str]], indexes: list[list[int]], game_matrix: list[list[str]]) -> list[list[int]]:
    valids = []
    for i in indexes:
        if 0 <= i[0] < len(matrix) and 0 <= i[1] < len(matrix[i[0]]) and game_matrix[i[0]][i[1]] == " ":
            valids.append(i)
    return valids

def check_defeat(matrix: list[list[str]], indexes: list[int], game_matrix: list[list[str]]) -> bool:
    value = matrix[indexes[0]][indexes[1]]

    if value < 0:
        game_matrix[indexes[0]][indexes[1]] = str(-1)
        return True
    elif value > 0:
        game_matrix[indexes[0]][indexes[1]] = str(value)
        return False
    else:
        game_matrix[indexes[0]][indexes[1]] = str(value)
        adjacents = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    adjacents.append([indexes[0]+i, indexes[1]+j])
        adjacents = valid_adjacents(matrix, adjacents, game_matrix)
        for i in adjacents:
            check_defeat(matrix, i, game_matrix)
        return False

def game() -> None:
    game_matrix: list[list[str]] = [[" " for _ in range(size)] for _ in range(size)]

    while check_empty_spaces(game_matrix) > bombs:
        print_matrix(game_matrix)
        indexes: list[int] = [int(i)-1 for i in input("- Indexes to check: ").split()]
        if check_defeat(matrix, indexes, game_matrix):
            print("Game Ended!")
            break

    print_matrix(game_matrix)

if __name__ == '__main__':
    game()
