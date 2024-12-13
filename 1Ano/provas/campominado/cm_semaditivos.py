from random import randint
from time import sleep
from typing import Callable

FLAG_CHARACTER: str = "⏴"
BOMB_CHARACTER: str = "X"

class Board:
    def __init__(self, size: tuple[int, int], amount_bombs: int, flag_char: str, bomb_char: str):
        self.size = size
        self.amount_bombs = amount_bombs
        self.__bombs_pos = []
        self.board = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.game_board = [[" " for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.generate_bombs(self.amount_bombs)
        self.__flag_char = flag_char
        self.__bomb_char = bomb_char
        self.__lost_game = False
    
    def generate_bombs(self, amount: int) -> None:
        """ Gera bombas aleatórias """
        self.amount_bombs = amount
        
        for _ in range(amount):
            pos: list[int] = [randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)]

            while self.board[pos[0]][pos[1]] == -1:
                pos = [randint(0, self.size[0] - 1), randint(0, self.size[1] - 1)]
            
            self.board[pos[0]][pos[1]] = -1

            self.__bombs_pos.append(pos)

            self.__expand_adjacents(pos)

    def __expand_adjacents(self, pos: tuple[int, int]) -> None:
        """ Aumenta o valor de "bombas próximas" em 1 para os quadradinhos adjacentes a bomba posicionada. """
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                if 0 <= pos[0] + i < self.size[0] and 0 <= pos[1] + j < self.size[1] and not self.board[pos[0] + i][pos[1] + j] == -1:
                    self.board[pos[0] + i][pos[1] + j] += 1

    def print_board(self) -> None:
        """ Printa o tabuleiro. """
        space_lines: int = len(str(self.size[0] - 1))

        print(f" {' ' * space_lines} | {' | '.join([str(i) for i in range(self.size[1])])} |")

        for i in range(self.size[0]):
            print(f" {i:<{space_lines}} ", end="|")

            for j in range(self.size[1]):
                space_columns: int = len(str(j))
                print(f" {self.game_board[i][j]:<{space_columns}} ", end="|")
                
            print()
    
    def toggle_flag(self, pos: tuple[int, int]) -> None:
        """ Coloca/Retira uma bandeira de uma posição. """
        if self.game_board[pos[0]][pos[1]] == self.__flag_char:
            self.game_board[pos[0]][pos[1]] = " "
        elif self.game_board[pos[0]][pos[1]] == " ":
            self.game_board[pos[0]][pos[1]] = self.__flag_char

    def check_pos(self, pos: tuple[int, int]) -> None:
        """ Verifica uma posição do jogo e a revala. """
        if self.game_board[pos[0]][pos[1]] == self.__flag_char: return

        if self.board[pos[0]][pos[1]] == -1:
            for i in self.__bombs_pos:
                self.game_board[i[0]][i[1]] = self.__bomb_char
            
            self.__lost_game = True
        elif self.board[pos[0]][pos[1]] == 0:
            self.game_board[pos[0]][pos[1]] = "0"
            
            positions = []
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if 0 <= pos[0] + i < self.size[0] and 0 <= pos[1] + j < self.size[1] and self.game_board[pos[0] + i][pos[1] + j] == " ":
                        positions.append((pos[0] + i, pos[1] + j))
            
            for i in positions:
                self.check_pos(i)
        else:
            self.game_board[pos[0]][pos[1]] = str(self.board[pos[0]][pos[1]])

    def check_lost(self) -> bool:
        """ Verifica a derrota do jogo. """
        if self.__lost_game: return True
    
    def check_end_game(self) -> bool:
        """ Verifica o fim do jogo. """
        empty_slots: int = 0
        
        for i in self.game_board:
            for j in i:
                if j == " " or j == self.__flag_char:
                    empty_slots += 1
        
        return empty_slots == self.amount_bombs

def play(board: Board) -> None:
    """ Joga o Jogo dos Tabuleiros. """
    is_flag: str = "n"
    pos: list[int] = [0, 0]

    while not board.check_end_game():
        board.print_board()

        print("-" * 30)

        try:
            is_flag = input("- Colocar/Retirar uma bandeira? (s/n): ").lower()

            if is_flag not in ["s", "n"]:
                raise ValueError("")
            
            for i in range(len(pos)):
                name_pos: str = "Linha" if i == 0 else "Coluna"

                pos[i] = int(input(f"- Posição da {name_pos}: "))

                if not 0 <= pos[i] < board.size[i]:
                    raise ValueError()
            
            if is_flag == "s":
                board.toggle_flag(pos)
            else:
                board.check_pos(pos)

                if board.check_lost():
                    print("Caiu em uma Bomba! :(")
                    break
        except ValueError:
            print("Valor Inválido!")
    else:
        print("Você Ganhou!")

    sleep(1)
    print("-" * 30)

    board.print_board()
    sleep(1)

def warn_chars() -> None:
    """ Gera um aviso e Permite a mudança dos caracteres de Bandeira e Bomba. """
    print(f"{f'Mudança de Caracteres':=^50}")
    
    global FLAG_CHARACTER, BOMB_CHARACTER
    print("Os tabuleiros desse jogo utilizam alguns caracteres UNICODE que podem não ser visualizados em alguns terminais ou aparecem relativamente 'estranhos', verifique se esses caracteres aparecem de forma correta:")
    print(f"Bandeira: {FLAG_CHARACTER}")
    print(f"Bomba...: {BOMB_CHARACTER}")
    option: str = input("Deseja alterar os caracteres? (s/n): ").lower()

    while option not in ["s", "n"]:
        print("Opção Inválida, tente novamente.")
        option: str = input("Deseja alterar os caracteres? (s/n): ").lower()
    
    if option == "s":
        FLAG_CHARACTER = input("Bandeira: ")
        BOMB_CHARACTER = input("Bomba...: ")

        while len(FLAG_CHARACTER) != 1 or len(BOMB_CHARACTER) != 1:
            print("Os caracteres precisam ter apenas 1 caractere de tamanho!")
            FLAG_CHARACTER = input("Bandeira: ")
            BOMB_CHARACTER = input("Bomba...: ")
        
        print("Troca realizada com sucesso!")

def play_normal_board() -> None:
    """ Joga com um tabuleiro normal retangular. """
    print(f"{f'Tabuleiro Normal':=^50}")

    global FLAG_CHARACTER, BOMB_CHARACTER
    board_size: list[int] = [0, 0]
    amount_bombs: int = 0

    while True:
        try:
            for i in range(len(board_size)):
                name_amount: str = "Linhas" if i == 0 else "Colunas"
                
                board_size[i] = int(input(f"- Quantidade de {name_amount} do Tabuleiro: "))

                if board_size[i] <= 0:
                    raise ValueError()
        
            amount_bombs = int(input("- Quantidade de Bombas: "))

            if amount_bombs <= 0 or amount_bombs > board_size[0] * board_size[1]:
                raise ValueError()
            
            break
        except ValueError:
            print("Valor Inválido!")

        print("-" * 30)

    print("-" * 30)
    
    board: Board = Board(board_size, amount_bombs, FLAG_CHARACTER, BOMB_CHARACTER)
    play(board)

def main_menu() -> Callable[[None], None] | None:
    """ Menu Principal do Jogo. """
    options: dict[int, Callable[[None], None]] = { i : ie for i, ie in enumerate([play_normal_board, warn_chars]) }
    
    while True:
        for i, ie in enumerate(["Jogar com Tabuleiro Normal", "Editar Caracteres", "Sair"]):
            print(f"{i+1} - {ie}")
        
        option: str = input("- Escolha uma das opções acima: ")

        try:
            opt: int = int(option) - 1

            if opt == len(options):
                return None
            elif options.get(opt) == None:
                raise ValueError()
            else:
                return options.get(opt)
        except ValueError:
            print("Opção Inválida!")
            print("-" * 30)

def game() -> None:
    """ Função Principal do Jogo. """
    warn_chars()

    while True:
        print(f"{f'Campo Minado':=^50}")

        selected_opt = main_menu()

        try:
            selected_opt()
        except:
            break

if __name__ == "__main__":
    game()
