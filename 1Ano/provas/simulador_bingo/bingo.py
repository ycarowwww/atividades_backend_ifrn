from random import randint

class Bingo:
    """Classe do jogo Bingo que contém a lógica principal de gerar números e cartelas."""
    def __init__(self):
        self._drawn_numbers = []
        self._players = []
        self._players_drawn_numbers = []
        self._needed_amount_numb = 0
    
    def generate_players(self, lines: int, columns: int, players_amount: int):
        """Gera as cartelas dos Jogadores."""
        self._needed_amount_numb = lines * columns
        
        for _ in range(players_amount):
            new_player = [ [ [] for _ in range(columns) ] for _ in range(lines) ]

            for c in range(columns):
                limits = (1 + 10 * c, 10 + 10 * c) # Define o intervalo dos números das colunas
                current_numbers = set() # Um Conjunto que contém os números já sorteados para evitar repetição nas colunas.

                for l in range(lines):
                    num = randint(limits[0], limits[1])
                    while num in current_numbers: # Se o número já for sorteado, então será necessário sortear outro.
                        num = randint(limits[0], limits[1])
                    current_numbers.add(num)

                    new_player[l][c] = num
            
            self._players.append(new_player)
            self._players_drawn_numbers.append([])

    def draw_number(self):
        """Sorteia uma dezena aleatória e verifica se ela está em alguma das cartelas."""
        columns = len(self._players[0][0])
        limits = (1, 10 * columns)

        num = randint(limits[0], limits[1])
        while num in self._drawn_numbers: # Verifica se esta dezena já não foi sorteada.
            num = randint(limits[0], limits[1])
        self._drawn_numbers.append(num)
        self._drawn_numbers.sort() # Deixa as dezenas sorteadas em ordem. Não é o melhor jeito em complexidade temporal, mas serve.

        for p in range(len(self._players)): # Verifica se alguma cartela contém este número.
            for l in self._players[p]:
                for c in l:
                    if c == num:
                        self._players_drawn_numbers[p].append(num)
                        continue
        
        return num

    def check_win(self):
        """Verifica se alguma cartela já foi completada."""
        winners = []
        for p in range(len(self._players)):
            if len(self._players_drawn_numbers[p]) >= self._needed_amount_numb:
                winners.append(p)
        return winners

    def get_players(self): return self._players

    def get_players_drawn_nums(self): return self._players_drawn_numbers

    def get_drawn_numbers(self): return self._drawn_numbers

def set_mode():
    """Define o modo de Jogo. Retorna a quantidade de linhas, colunas e jogadores do modo."""
    print("Indique o Modo de Jogo:")
    print(" 0 - Rápido \n 1 - Demorado \n 2 - Sair do Jogo")
    mode = input(" => ")

    while mode not in ["0", "1", "2"]:
        print("Opção Inválida, Tente Novamente!")
        mode = input(" => ")
    
    if mode == "0":
        return (2, 3, 2)
    elif mode == "1":
        return (3, 4, 4)
    else:
        return None

def print_players(players, players_drawn_nums):
    """Printa as cartelas dos jogadores."""
    for ip, p in enumerate(players):
        print(f"Jogador {ip+1}:")

        for l in p:
            for c in l:
                if c in players_drawn_nums[ip]:
                    print(f"({c:02d})", end="")
                else:
                    print(f" {c:02d} ", end="")
            print()
        print()

def main():
    game = Bingo()

    mode = set_mode()
    if mode == None: return
    
    game.generate_players(mode[0], mode[1], mode[2])
    
    last_draw_num = game.draw_number()
    
    while True:
        print_players(game.get_players(), game.get_players_drawn_nums())
        
        print(f"=> Última dezena sorteada: {last_draw_num:02d}")
        print(f"Dezenas sorteadas até o momento: {' '.join([f'{i:02d}' for i in game.get_drawn_numbers()])}")

        if len(game.check_win()) != 0: # Verifica se alguma cartela foi completada.
            break

        input("Digite ENTER para continuar")
        
        last_draw_num = game.draw_number()

    print(f"\n{'='*30}\n")
    
    for p in game.check_win():
        print(f"Jogador {p+1} é o ganhador!")

if __name__ == '__main__':
    main()
