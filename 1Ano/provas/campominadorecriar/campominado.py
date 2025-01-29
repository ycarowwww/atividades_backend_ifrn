from random import randint

def menu() -> int:
    """Mostra o Menu do Jogo para selecionar o nível de dificuldade e retorna quantidade de bombas."""
    option: str = ""
    while option not in ["1", "2", "3"]:
        print("Informe o Nível de Dificuldade:")
        print(" 1 - Fácil (uma bomba) \n 2 - Médio (duas bombas) \n 3 - Difícil (três bombas)")
        option = input()
    return int(option)

def add_bomb(board: list[list[str]]) -> None:
    """Adiciona uma bomba em uma posição aleatória do Tabuleiro e aumenta os valores das posições adjacentes."""
    lines: int = len(board)
    columns: int = len(board[0])
    pos: list[int] = [randint(0, lines-1), randint(0, columns-1)]
    board[pos[0]][pos[1]] = "*"

    adjacent_pos: list[list[int]] = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= pos[0] + i < lines and  0 <= pos[1] + j < columns and not (i == 0 and j == 0):
                adjacent_pos.append([pos[0] + i, pos[1] + j])
    
    for p in adjacent_pos:
        if board[p[0]][p[1]] != "*":
            board[p[0]][p[1]] = str(int(board[p[0]][p[1]]) + 1)

def print_board(game_board: list[list[str]]) -> None:
    """Mostra o Tabuleiro"""
    lines: int = len(game_board)
    columns: int = len(game_board[0])
    print(f"  {' '.join([str(i) for i in range(columns)])}")
    for i in range(lines):
        print(f"{i}|{'|'.join([str(i) for i in game_board[i]])}|")

def check_win(game_board: list[list[str]], bombs: int) -> bool:
    """Verifica se a quantidade de espaços não verificados é igual a quantidade de bombas (verifica a vitória)."""
    unchecked_spaces: int = 0
    for i in game_board:
        for j in i:
            if j == "?":
                unchecked_spaces += 1
    return unchecked_spaces == bombs

def show_position(game_board: list[list[str]], board: list[list[str]], pos: list[int]) -> str:
    """Mostra a Posição Marcada do Tabuleiro."""
    game_board[pos[0]][pos[1]] = board[pos[0]][pos[1]]
    return game_board[pos[0]][pos[1]]

def show_bombs(game_board: list[list[str]], board: list[list[str]]) -> None:
    """Revela todas as bombas."""
    for iind, i in enumerate(board):
        for jind, j in enumerate(i):
            if j == "*":
                game_board[iind][jind] = "*"

def game() -> None:
    """Função principal do Jogo."""
    bombs: int = menu()
    board: list[list[str]] = [["0" for _ in range(4)] for _ in range(3)]
    game_board: list[list[str]] = [["?" for _ in range(4)] for _ in range(3)]
    for _ in range(bombs):
        add_bomb(board)

    check_position: list[int] = [0, 0]
    while not check_win(game_board, bombs):
        print_board(game_board)

        try:
            check_position[0] = int(input(" Informe a linha:\n"))
            check_position[1] = int(input(" Informe a coluna:\n"))
            if not (0 <= check_position[0] < len(game_board) and 0 <= check_position[1] < len(game_board[0])):
                raise IndexError()
        except (ValueError, IndexError):
            print("Jogada Inválida")
            continue
            
        if show_position(game_board, board, check_position) == "*":
            show_bombs(game_board, board)
            print_board(game_board)
            print("BUM! Você perdeu :(")
            break
    else:
        print_board(game_board)
        print("Você sobreviveu! \\o/")

if __name__ == '__main__':
    game()
